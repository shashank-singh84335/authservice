from authapis.utils import AuthSevice, UserProfileService
import logging
from authapis.helpers import get_response, CustomExceptionHandler
from authapis.status_code import success
from authapis.status_code import Statuses
from authapis.constants import *
import re
from django.db import transaction

logger = logging.getLogger("django")


class SignUpService(UserProfileService, AuthSevice):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.secret = self.get_email_password()

    def verify_credential(self, credential_obj):
        if credential_obj and int(self.type) == CREDENTIAL_TYPES[EMAIL_PASSWORD]:
            raise CustomExceptionHandler(Statuses.credential_already_exists)
        return credential_obj

    def create_profile(self, otp_key):
        logger.debug('get_user_token')

        user_auth_obj = self.create_user_auth()
        logger.debug('user_auth_obj: %s' % user_auth_obj)

        secret = self.salt_and_hash(prefix=user_auth_obj.user_id, secret=self.secret)
        logger.debug('secret: %s' % secret)

        credential_obj = self.create_credential(user_auth=user_auth_obj, secret=secret or otp_key)
        logger.debug('credential_obj created: %s' % credential_obj)

        return user_auth_obj, secret, credential_obj
    
    @transaction.atomic
    def get_response(self):
        otp_key = None 
        if int(self.type) == CREDENTIAL_TYPES[PHONE_OTP]:
            otp_key, otp = self.generate_otp()
            logger.debug(f'otp {otp}')

        credential_obj = self.verify_credential(self.get_credential())
        logger.debug('credential_obj: %s' % credential_obj)
        if credential_obj:
            credential_obj = self.update_code_genration_attempt_and_otp(credential_object=self.verify_login_rate_limit(credential_obj), otp_key=otp_key)
        else:
            user_auth_obj, secret, credential_obj = self.create_profile(otp_key=otp_key)
        
        return get_response(success)
    
