from django.contrib import admin

# Register your models here.
from api.models import FavoriteQuote, FavoriteCharacter


@admin.register(FavoriteCharacter)
class FavoriteCharacterAdmin(admin.ModelAdmin):
    fields = (
        "user", "character", "created", "updated",
    )
    list_display = (
        "user", "character", "created", "updated",

    )
    readonly_fields = (
        "created", "updated",
    )


@admin.register(FavoriteQuote)
class FavoriteQuoteAdmin(admin.ModelAdmin):
    fields = (
        "user", "quote", "created", "updated",
    )
    list_display = (
        "user", "created", "updated",

    )
    readonly_fields = (
        "created", "updated",
    )
