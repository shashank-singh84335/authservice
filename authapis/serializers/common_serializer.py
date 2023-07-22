from rest_framework import serializers
from authapis.serializers import CustomCharField, CustomIntegerField
from authapis.models.credential_model import Credential
from authapis.constants import CREDENTIAL_TYPES
from authapis.helpers import help_text_for_dict, common_checking_and_passing_value_from_list_dict
from authapis.status_code import Statuses


class SuccessResponseSerializer(serializers.Serializer):
    status = CustomIntegerField(required=True)
    message = CustomCharField(required=True)

class CredentialHeadSerializer(serializers.ModelSerializer):
    credential = CustomCharField(required=True, allow_blank=False)
    type = CustomCharField(required=True, help_text=help_text_for_dict(CREDENTIAL_TYPES), allow_blank=False)
    secret = CustomCharField(allow_blank=False, required=False, store_lower=False)

    def validate_type(self, value):
        return common_checking_and_passing_value_from_list_dict(value, CREDENTIAL_TYPES, Statuses.credential_type_invalid)


    class Meta:
        model = Credential
        fields = '__all__'