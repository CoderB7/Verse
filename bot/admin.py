from django.contrib import admin

from .models import TelegramChatInfo, TelegramUser

@admin.register(TelegramChatInfo)
class TelegramInfoAdmin(admin.ModelAdmin):
    list_display = ["chat_id", "chat_title", "chat_type"]
    search_fields = ["chat_title"]
    list_filter = ["chat_type"]


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "first_name",
        "last_name",
        "username",
    )
    list_display_links = ("user_id",)
