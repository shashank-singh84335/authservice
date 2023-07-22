from django.db import models
from authapis.models import UserAuth, CommonModel

class Credential(CommonModel,models.Model):
    credential = models.TextField(primary_key=True)
    secret = models.TextField(null=True)
    type = models.PositiveSmallIntegerField(null=False)
    user_auth = models.ForeignKey('UserAuth', to_field='user_id', on_delete=models.RESTRICT, null=False)
    last_code_generation_attempt = models.DateTimeField(null=True)
    consecutive_code_generation_attempt_counter = models.PositiveSmallIntegerField(null=False)
    last_code_verification_attempt = models.DateTimeField(null=True)
    consecutive_code_verification_attempt_counter = models.PositiveSmallIntegerField(null=False)
    
