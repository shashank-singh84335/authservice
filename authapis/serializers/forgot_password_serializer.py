from authapis.serializers import  CredentialHeadSerializer
from authapis.serializers import CustomCharField
from authapis.constants import FORGOT_PASSWORD_REQUEST_TYPES
from authapis.helpers import common_checking_and_passing_value_from_list_dict, help_text_for_dict
from authapis.status_code import Statuses

class ForgotPasswordRequestSerializer(CredentialHeadSerializer):
    type = CustomCharField(required=True, help_text=help_text_for_dict(FORGOT_PASSWORD_REQUEST_TYPES), allow_blank=False)

    def validate_type(self, value):
        common_checking_and_passing_value_from_list_dict(value, FORGOT_PASSWORD_REQUEST_TYPES, Statuses.credential_type_invalid)
        return value

    class Meta(CredentialHeadSerializer.Meta):
        fields = ('credential',"type", "secret")