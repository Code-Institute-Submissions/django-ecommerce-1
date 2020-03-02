from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        *UserAdmin.fieldsets,
        ('Additional personal info', {
            'fields': ('address',
                       'city', 'country', 'post_code', 'date_of_birth',)
        }),
    )

    form = CustomUserChangeForm
    fieldsets = (
        *UserAdmin.fieldsets,
        ('Additional personal info', {
            'fields': ('address',
                       'city', 'country', 'post_code', 'date_of_birth',)
        }),
    )
    model = CustomUser


admin.site.register(CustomUser, CustomUserAdmin)
