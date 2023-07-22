
from django.db import models
from authapis.constants import STATUS_ACTIVE, CREATION_BY

class CommonModel(models.Model):
    status = models.PositiveSmallIntegerField(null=False, default=STATUS_ACTIVE)
    creation_date = models.DateTimeField(null=False, auto_now_add=True)
    created_by = models.TextField(null=False, default=CREATION_BY)
    updation_date = models.DateTimeField(null=True, auto_now=True)
    updation_by = models.TextField(null=True)

    class Meta:
        abstract = True