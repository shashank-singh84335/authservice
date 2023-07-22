from authapis.serializers import SuccessResponseSerializer, CustomCharField
from authapis.models import RefreshToken
from rest_framework import serializers


class RefreshTokenRequestSerializer(serializers.Serializer):
    refresh_token = CustomCharField(required=True, store_lower=False)


class TokenSerializer(serializers.Serializer):
    access_token = CustomCharField(required=True, store_lower=False)
    refresh_token = CustomCharField(required=True, store_lower=False)

class TokenResponseSerializer(SuccessResponseSerializer):
    data = TokenSerializer()
    