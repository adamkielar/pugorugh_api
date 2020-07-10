from django.contrib import admin

from pugorugh import models

admin.site.register(models.Dog)
admin.site.register(models.UserPref)
admin.site.register(models.UserDog)
