from authapis.serializers import  CredentialHeadSerializer
from authapis.serializers import serializers


class SignUpRequestSerializer(CredentialHeadSerializer):

    class Meta(CredentialHeadSerializer.Meta):
        fields = ('credential',"secret","type")



class SignInRequestSerializer(CredentialHeadSerializer):
    secret = serializers.CharField(allow_blank=False, required=False)

    class Meta(CredentialHeadSerializer.Meta):
        fields = ('credential',"secret","type")