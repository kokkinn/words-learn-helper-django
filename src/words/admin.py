from django.contrib import admin
from .models import Word, GroupOfWords, Result


class WordsInline(admin.TabularInline):
    model = Word.group.through


class GroupAdmin(admin.ModelAdmin):
    model = GroupOfWords
    inlines = [
        WordsInline,
    ]


admin.site.register(Word)
admin.site.register(GroupOfWords, GroupAdmin)
admin.site.register(Result)