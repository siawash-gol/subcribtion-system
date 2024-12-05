from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from config.auth.Users.models import User
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class AdminUser(UserAdmin):
    list_display = ("email", "role",
                    "verified_email", 'auth_provider')
    fieldsets = (
        (None, {"fields": ("username", "password","slug")}),
        (_("Personal info"), {"fields": ("email",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "role",
                    "verified_email",
                    "auth_provider",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
