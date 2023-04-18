from django.contrib import admin
from .models import TranslatedVariables


@admin.register(TranslatedVariables)
class TVAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "korean_word",
        "translated_variable",
    )
    list_display_links = (
        "id",
        "korean_word",
        "translated_variable",
    )
