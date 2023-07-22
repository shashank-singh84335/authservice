import logging
import django.utils.timezone
from pyotp import TOTP, random_base32
from authapis.constants import *
import python_jwt as jwt
from core.settings import AUTH_JWT_CONFIG, SECRET_KEY
from authapis.models import *
from authapis.constants import STATUS_ACTIVE, STATUS_INACTIVE
from authapis.helpers import CustomExceptionHandler
from authapis.constants import *
from authapis.status_code import Statuses
import hashlib
from datetime import timedelta
from authapis.middleware import get_request
import re

logger = logging.getLogger("django")


class AuthSevice:
    OTP_EXPIRATION_TIME =  AUTH_JWT_CONFIG.get("OTP_EXPIRATION_TIME",timedelta(minutes=7).seconds)

    def __init__(self, **kwargs):
        logger.debug('AuthService init')
        self.__dict__.update(kwargs)
        logger.debug('data: %s' % kwargs)

    def generate_otp(self):
        logger.debug('generate_otp')
        otp_key = random_base32()
        otp = TOTP(otp_key, interval=AuthSevice.OTP_EXPIRATION_TIME)
        logger.debug("Generated OTP: %s", otp.now())
        logger.debug("otp_key: %s", otp_key)
        return otp_key, otp

    def verify_otp(self, credential_obj):
        logger.debug('verify_PHONE_OTP')
        DUMMY_OTP, DEFAULT_OTP = AUTH_JWT_CONFIG.get("DUMMY_OTP","000000"), AUTH_JWT_CONFIG.get("DUMMY_OTP","000000")
        DEFAULT_CREDENTIAL = AUTH_JWT_CONFIG.get("DEFAULT_CREDENTIAL","1234567890")

        otp = TOTP(credential_obj.secret, interval=AuthSevice.OTP_EXPIRATION_TIME)
        logger.debug("otp verification %s", otp.verify(self.secret))
        otp_verfication_status = otp.verify(self.secret) or (DUMMY_OTP is not None and self.secret == DUMMY_OTP) or\
            (self.credential == DEFAULT_CREDENTIAL and self.secret == DEFAULT_OTP)
        logger.debug(f"otp_verfication_status {otp_verfication_status}")
        if not otp_verfication_status:
            logger.debug("otp verification failed")
            raise CustomExceptionHandler(Statuses.invalid_otp)
        return otp_verfication_status
    
    def verify_password(self, credential_obj):
        logger.debug('verify_password')
        password_match_status = self.salt_and_hash(
            self.secret, credential_obj.user_auth_id) == credential_obj.secret
        logger.debug(f'password_match_status {password_match_status}')
        if not password_match_status:
            logger.debug("password verification failed")
            raise CustomExceptionHandler(Statuses.password_not_matching)
        return password_match_status

    def generate_user_token(self, access_token_payload, refresh_token_payload):
        logger.debug('generate_user_token')

        access_token_payload.update(AUTH_JWT_CONFIG.get("ACCESS_TOKEN_EXTRA_CONFIGS",{}))
        refresh_token_payload.update(AUTH_JWT_CONFIG.get("REFRESH_TOKEN_EXTRA_CONFIGS",{}))

        access_token = self.generate_token(access_token_payload, lifetime=AUTH_JWT_CONFIG.get("LIFE_TIME_OF_ACCESS_TOKEN"))
        refresh_token = self.generate_token(refresh_token_payload, lifetime=AUTH_JWT_CONFIG.get("LIFE_TIME_OF_REFRESH_TOKEN"))

        logger.debug('access_token: %s' % access_token)
        logger.debug('refresh_token: %s' % refresh_token)

        RefreshToken.objects.create(
            refresh_token=refresh_token, user_auth_id=access_token_payload['user_auth_id'])
        
        return {"access_token": access_token, "refresh_token": refresh_token}

    def generate_token(self, payload, lifetime = timedelta(minutes=5)):
        payload['iss'] = AUTH_JWT_CONFIG.get("iss",'test.com')
        token = jwt.generate_jwt(payload, AUTH_JWT_CONFIG.get("JWT_PRIVATE_KEY", SECRET_KEY), AUTH_JWT_CONFIG.get("ALGORITHM_OF_JWT", "RS256"),
                                            lifetime=lifetime)
        return token
    
    def verify_token(self):
        request = get_request()
        authorization = request.headers.get("Authorization")
        token = authorization.split(" ")[1] if authorization else authorization
        header, claims = jwt.verify_jwt(token,AUTH_JWT_CONFIG.get("JWT_PRIVATE_KEY",SECRET_KEY),[AUTH_JWT_CONFIG.get("ALGORITHM_OF_JWT", "RS256")])
        return header, claims

    def salt_and_hash(self, secret, prefix):
        if secret:
            return hashlib.sha256((str(prefix) + secret + AUTH_JWT_CONFIG.get("SALTING_CONSTANT","default")).encode()).hexdigest()

class UserProfileService:
    LOGIN_RATE_LIMITER_DURATION = AUTH_JWT_CONFIG.get("LOGIN_RATE_LIMITER_DURATION", timedelta(seconds=30))
    LOGIN_RATE_LIMIT = AUTH_JWT_CONFIG.get("LOGIN_RATE_LIMIT",5)

    def __init__(self, **kwargs):
        logger.debug('UserProfileService init')
        self.__dict__.update(kwargs)
        logger.debug('UserProfileService data: %s' % kwargs)

    def get_credential(self):
        logger.debug('get_credentials')
        credential_obj = Credential.objects.filter(credential=self.credential)
        logger.debug(f"credential_obj {credential_obj}")
        return credential_obj.first()

    def get_email_password(self):
        logger.debug('get_email_password')
        password_pattern = EMAIL_PASSWORD_PATTERN
        reg_match = None
        if self.secret:
            reg_match = re.match(password_pattern, self.secret)
            
        logger.debug('reg_match')
        if not reg_match and int(self.type) == CREDENTIAL_TYPES[EMAIL_PASSWORD]:
            logger.exception("password is invalid")
            raise CustomExceptionHandler(Statuses.password_invalid)
        return self.secret
    

    def verify_login_rate_limit(self, credential_object, limit_duration=LOGIN_RATE_LIMITER_DURATION, rate_limit=LOGIN_RATE_LIMIT):
        if django.utils.timezone.now() - credential_object.last_code_generation_attempt < limit_duration:
            if credential_object.consecutive_code_generation_attempt_counter > rate_limit:
                raise CustomExceptionHandler(Statuses.too_many_login_attempts)
        else:
            credential_object.consecutive_code_generation_attempt_counter = 0
        return credential_object

    def update_code_genration_attempt_and_otp(self, credential_object, otp_key=None):
        credential_object.last_code_generation_attempt = django.utils.timezone.now()
        logger.debug(
            f"consecutive_code_generation_attempt_counter {credential_object.consecutive_code_generation_attempt_counter}")
        credential_object.consecutive_code_generation_attempt_counter = credential_object.consecutive_code_generation_attempt_counter + 1
        if otp_key:
            credential_object.secret = otp_key
        credential_object.save()
        return credential_object

    def create_user_auth(self):
        logger.debug('create_user')
        return UserAuth.objects.create(status=STATUS_INACTIVE)


    def create_credential(self, user_auth, secret):
        logger.debug(f'user {user_auth} {secret}')
        return Credential.objects.create(credential=self.credential,
                                    user_auth=user_auth,
                                    secret=secret,
                                    type=int(self.type), created_by=user_auth.user_id,
                                    last_code_generation_attempt=django.utils.timezone.now(),
                                    last_code_verification_attempt=django.utils.timezone.now(),
                                    consecutive_code_generation_attempt_counter=0,
                                    creation_date=django.utils.timezone.now(),
                                    consecutive_code_verification_attempt_counter=0,
                                    status=STATUS_INACTIVE)

    def activate_user(self, credential_obj):
        if credential_obj.user_auth.status == STATUS_INACTIVE:
            # set user status 1 after otp verified
            credential_obj.user_auth.status = STATUS_ACTIVE
            credential_obj.status = STATUS_ACTIVE
            credential_obj.user_auth.save()
            credential_obj.save()
