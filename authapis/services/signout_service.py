from authapis.models import RefreshToken
from authapis.status_code import success
from authapis.helpers import get_response

def signout_service(serializer_data):
    refresh_token_obj = RefreshToken.objects.get(refresh_token = serializer_data['refresh_token'])
    RefreshToken.objects.filter(user_auth = refresh_token_obj.user_auth).delete()
    return get_response(success)