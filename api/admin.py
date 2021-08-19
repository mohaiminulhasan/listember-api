from typing import List
from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.List)
admin.site.register(models.ListItem)
admin.site.register(models.Profile)
admin.site.register(models.Invite)