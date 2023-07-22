from django.db import models
from authapis.models import UserAuth, CommonModel


class RefreshToken(CommonModel,models.Model):
    refresh_token = models.TextField(primary_key=True)
    user_auth = models.ForeignKey("UserAuth", to_field='user_id', on_delete=models.RESTRICT, null=False)
