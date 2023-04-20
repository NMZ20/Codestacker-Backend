from django.contrib import admin
from . import models


class File(admin.ModelAdmin):
    fields = ("id", "name", "upload_time")


admin.site.register(models.File)
admin.site.register(models.Sentence)
