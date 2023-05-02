from django.contrib import admin

from . import models


class WordAdmin(admin.ModelAdmin):
    list_display = ['pk', 'en_word', 'ru_translation']
    list_editable = ['en_word', 'ru_translation']


admin.site.register(models.Words, WordAdmin)
