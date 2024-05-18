from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import *
# Register your models here.
admin.site.register(Article)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'school')
    
    def get_queryset(self, request):
        if request.user.is_superuser:
            return CustomUser.objects.all()
        else:
            return CustomUser.objects.filter(username=request.user.username)
