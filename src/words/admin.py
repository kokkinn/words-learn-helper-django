from django.contrib import admin

from accounts.models import CustomUser
from .models import Word, GroupOfWords, Result


class WordsInline(admin.TabularInline):
    model = Word.groups.through
    readonly_fields = ('id',)


class UserInline(admin.TabularInline):
    model = CustomUser


class GroupAdmin(admin.ModelAdmin):
    model = GroupOfWords
    inlines = [
        WordsInline, UserInline,
    ]


class WordAdmin(admin.ModelAdmin):
    model = Word
    readonly_fields = ('created_date',)


admin.site.register(Word, WordAdmin)
admin.site.register(GroupOfWords, GroupAdmin)
admin.site.register(Result)
