from django.contrib import admin
from .models import Variables, AbbreviatedVariables


@admin.register(Variables)
class VAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "searched_variable",
        "count",
    )
    list_display_links = (
        "id",
        "searched_variable",
        "count",
    )


@admin.register(AbbreviatedVariables)
class AVAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "variable",
        "abbreviated_variable",
    )
    list_display_links = (
        "id",
        "variable",
        "abbreviated_variable",
    )
