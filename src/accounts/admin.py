from django.contrib import admin

from words.models import GroupOfWords
from .models import CustomUser  # Register your models here.


class GroupsInline(admin.TabularInline):
    model = GroupOfWords


class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    inlines = [
        GroupsInline,
    ]


admin.site.register(CustomUser, CustomUserAdmin)
