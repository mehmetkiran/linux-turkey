from django.contrib import admin
from .models import *


@admin.register(ContacUsModel)
class ContacUsAdmin(admin.ModelAdmin):
    list_display = ['contacID', 'name', 'email', 'website', 'message', ]

