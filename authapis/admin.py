from django.contrib import admin
from authapis.models import *
# Register your models here.

admin.site.register(UserAuth)
admin.site.register(Credential)
admin.site.register(RefreshToken)
