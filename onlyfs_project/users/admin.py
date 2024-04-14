from django.contrib import admin
from users.models import CustomUser, Role




admin.site.register(CustomUser)
admin.site.register(Role)