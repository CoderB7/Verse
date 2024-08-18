from core.settings.base import *

DEBUG = False

# ALLOWED_HOSTS = [
#     "cura.falconsoft.uz",
# ]

# CSRF_TRUSTED_ORIGINS = [
#     "https://cura.falconsoft.uz",
# ]
# CSRF_COOKIE_SECURE = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASS"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

# LOGGER_BOT_TOKEN = env.str("LOGGER_BOT_TOKEN")
# LOGGER_CHAT_ID = env.str("LOGGER_CHAT_ID")

# CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_HEADERS = ["*"]