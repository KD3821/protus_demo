from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'uuid', 'oauth_verified', 'is_active', 'is_staff', 'created_at', 'is_verified']
