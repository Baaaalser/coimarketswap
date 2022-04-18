from django.contrib import admin

# Register your models here.

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

admin.site.unregister(Group)  # no me interesan los grupos desde el panel

@admin.register(get_user_model()) # Si no pongo esto no puedo administrar usuario desde admin por usar un custom
class CustomUserAdmin(UserAdmin):
    pass