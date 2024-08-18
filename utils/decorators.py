from bot.models import TelegramUser


def get_user(func):
    def wrap(update, context, *args, **kwargs):
        try:
            user_id = update.message.chat_id
        except AttributeError:
            user_id = update.callback_query.message.chat_id

        user, created = TelegramUser.objects.get_or_create(
            user_id=user_id,
            defaults={
                "username": update.effective_user.username,
                "first_name": update.effective_user.first_name,
                "last_name": update.effective_user.last_name,
            },
        )
        return func(update, context, user, *args, **kwargs)

    return wrap
