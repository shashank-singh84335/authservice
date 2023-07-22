from authapis.utils import AuthSevice, UserProfileService
import logging
from authapis.constants import CREDENTIAL_TYPES, EMAIL_PASSWORD
from authapis.constants import STATUS_ACTIVE
from authapis.status_code import success
from authapis.helpers import CustomExceptionHandler, get_response
from authapis.status_code import Statuses
from django.db import transaction
from core.settings import AUTH_JWT_CONFIG
from datetime import timedelta

logger = logging.getLogger("django")


class ForgotPasswordService(AuthSevice, UserProfileService):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def generate(self, credential_obj):
        otp_key, otp = self.generate_otp()
        logger.debug(f'OTP - {otp}')
        credential_obj = self.update_code_genration_attempt_and_otp(self.verify_login_rate_limit(credential_obj), otp_key=otp_key)
        return get_response(success)
    
    def verify_credential(self, credential_obj):
        if not credential_obj or credential_obj.status != STATUS_ACTIVE:
            raise CustomExceptionHandler(Statuses.invalid_credential)
        if credential_obj.type != CREDENTIAL_TYPES[EMAIL_PASSWORD]:
            raise CustomExceptionHandler(Statuses.parameter_error)
        return credential_obj

    def generate_forgot_password_payload(self, credential_obj):
        payload = {"user_id": str(credential_obj.user_auth_id), "sub": AUTH_JWT_CONFIG.get("FORGOT_PASSWORD_SUB",'reset_password')}
        payload.update(AUTH_JWT_CONFIG.get("FORGOT_PASSWORD_TOKEN_EXTRA_CONFIGS",{}))
        return payload

    def validate(self,credential_obj):
        if not self.secret:
            raise CustomExceptionHandler(Statuses.invalid_otp)
        
        credential_obj = self.verify_login_rate_limit(credential_obj,limit_duration =AUTH_JWT_CONFIG.get("FORGOT_PASSWORD_LIMITER_DURATION",timedelta(seconds=30)),
                                                                rate_limit = AUTH_JWT_CONFIG.get("FORGOT_PASSWORD_RATE_LIMIT",5))
        credential_obj = self.update_code_genration_attempt_and_otp(credential_obj)
        self.verify_otp(credential_obj=credential_obj)
        token = self.generate_token(self.generate_forgot_password_payload(credential_obj),lifetime = AUTH_JWT_CONFIG.get("FORGOT_PASSWORD_JWT_EXPIRATION",timedelta(minutes=10)))
        access_token = {"access_token":token}
        return get_response(success, access_token)

    def reset_password(self, claims, secret, cred):
        jwt_user_id = claims["user_id"]
        jwt_type = claims["sub"]
        print(jwt_user_id, str(cred.user_auth.user_id), "---",jwt_type, AUTH_JWT_CONFIG.get("FORGOT_PASSWORD_SUB",'reset_password'))
        if jwt_user_id == str(cred.user_auth.user_id) and jwt_type == AUTH_JWT_CONFIG.get("FORGOT_PASSWORD_SUB",'reset_password'):
            print("in funct")
            cred.secret = secret
            cred.save()
            return get_response(success)
        else:
            raise CustomExceptionHandler(Statuses.parameter_error)

    def reset(self, credential_obj):
        self.type = CREDENTIAL_TYPES[EMAIL_PASSWORD]
        self.get_email_password()
        secret = self.salt_and_hash(prefix=credential_obj.user_auth.user_id, secret=self.secret)
        header, claims = self.verify_token()
        return self.reset_password(claims, secret, credential_obj)
        
    @transaction.atomic
    def get_response(self):
        credential_obj = self.verify_credential(self.get_credential())
        function = getattr(self, self.type)
        return function(credential_obj)
