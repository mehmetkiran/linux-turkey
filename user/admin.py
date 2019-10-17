from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import UserModel


@admin.register(UserModel)
class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    model = UserModel
    list_display = ['email', 'username', 'userAbout', ]
    list_display_links = ['email', 'username', 'userAbout', ]
