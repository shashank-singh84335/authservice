from authapis.utils import AuthSevice, UserProfileService
import logging
from authapis.constants import *
from authapis.status_code import success
from authapis.helpers import get_response
from authapis.models import RefreshToken

logger = logging.getLogger("django")


class RefreshTokenService(AuthSevice, UserProfileService):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def generate_token_payload(self, refresh_token_obj, roles=[DEFAULT_USER_ROLE]):
        logger.debug("Generating token payload")
        user_auth_id = str(refresh_token_obj.user_auth_id)
        access_token_payload = {"user_auth_id": user_auth_id, "roles": roles}
        logger.debug("access_token_payload  = %s", access_token_payload)
        refresh_token_payload =  {"user_id": user_auth_id}
        logger.debug("referesh_token_payload = %s", refresh_token_payload)
        return access_token_payload, refresh_token_payload
    
    def get_token(self):
        refresh_token_obj =  RefreshToken.objects.get(refresh_token=self.refresh_token)
        RefreshToken.objects.filter(user_auth=refresh_token_obj.user_auth).delete()
        access_token_payload, refresh_token_payload = self.generate_token_payload(refresh_token_obj)
        return get_response(success,self.generate_user_token(access_token_payload, refresh_token_payload))
        