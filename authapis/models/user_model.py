from uuid import uuid4
from authapis.models import CommonModel
from django.db import models


class UserAuth(CommonModel,models.Model):
    user_id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid4)
