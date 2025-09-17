from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.models import User, Otp
from account.forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    # فرم‌ها برای اضافه و تغییر کاربر
    form = UserChangeForm
    add_form = UserCreationForm

    # فیلدهایی که در لیست نمایش داده می‌شوند
    list_display = ["phone", "email", "full_name", "is_admin", "is_staff", "is_superuser", "is_active"]
    list_filter = ["is_admin", "is_staff", "is_superuser", "is_active"]

    fieldsets = [
        (None, {"fields": ["phone", "email", "password"]}),
        ("Personal info", {"fields": ["full_name"]}),
        ("Permissions", {"fields": ["is_active", "is_admin", "is_staff", "is_superuser"]}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["phone", "email", "full_name", "password1", "password2", "is_active", "is_admin", "is_staff",
                           "is_superuser"],
            },
        ),
    ]

    search_fields = ["phone", "email", "full_name"]
    ordering = ["phone"]
    filter_horizontal = []


# ثبت UserAdmin
admin.site.register(User, UserAdmin)
admin.site.register(Otp)

# حذف گروه‌ها از ادمین چون استفاده نمی‌شوند
admin.site.unregister(Group)
