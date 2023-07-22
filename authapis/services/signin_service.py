from authapis.utils import AuthSevice, UserProfileService
import logging
from authapis.helpers import get_response, CustomExceptionHandler
from authapis.status_code import success
from authapis.constants import *
from authapis.status_code import Statuses
from core.settings import AUTH_JWT_CONFIG
from django.db import transaction

logger = logging.getLogger("django")

class SignInService(UserProfileService, AuthSevice):
    _PASSWORD_VERIFICATION_CONFIG = {
        CREDENTIAL_TYPES[EMAIL_PASSWORD] : 'verify_password',
        CREDENTIAL_TYPES[PHONE_OTP] : 'verify_otp',
    }

    def __init__(self,**kwargs):
        logger.debug("Creating SignInService")
        super().__init__(**kwargs)


    def verify_credential(self, credential_obj):
        logger.debug("Verifying credential")
        if not credential_obj:
            raise CustomExceptionHandler(Statuses.invalid_credential)
        return credential_obj

    def generate_token_payload(self, credential_obj, roles=[DEFAULT_USER_ROLE]):
        logger.debug("Generating token payload")
        user_auth_id = str(credential_obj.user_auth_id)
        access_token_payload = {"user_auth_id": user_auth_id, "roles": roles}
        logger.debug("access_token_payload  = %s", access_token_payload)
        refresh_token_payload =  {"user_id": user_auth_id}
        logger.debug("referesh_token_payload = %s", refresh_token_payload)
        return access_token_payload, refresh_token_payload


    def verify_secret(self, credential_obj):
        function_name = SignInService._PASSWORD_VERIFICATION_CONFIG[int(self.type)]
        function = getattr(self,function_name)
        return function(credential_obj)

    @transaction.atomic
    def get_user_token(self):
        logger.debug("get_user_token")
        credential_obj = self.verify_credential(self.get_credential())
        # roles = self.verify_role(credential_obj)
        self.verify_secret(credential_obj=credential_obj)
        self.update_code_genration_attempt_and_otp(credential_object=self.verify_login_rate_limit(credential_obj))
        self.activate_user(credential_obj)
        access_token_payload, refresh_token_payload = self.generate_token_payload(credential_obj)
        return get_response(success,self.generate_user_token(access_token_payload, refresh_token_payload))

