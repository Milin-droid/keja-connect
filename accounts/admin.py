
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        ('KejaConnect Information', {
            'fields': ('role', 'phone_number')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('KejaConnect Information', {
            'fields': ('role', 'phone_number')
        }),
    )

    list_display = [
        'username',
        'email',
        'role',
        'phone_number',
        'is_staff',
        'is_active',
    ]

    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'phone_number']
