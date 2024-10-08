from core.settings.base import *

DEBUG = False

ALLOWED_HOSTS = [
    "*",
]

CSRF_TRUSTED_ORIGINS = [
    "https://verse.userb.uz",
]
CSRF_COOKIE_SECURE = True

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

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', 6380)], # change it to 'redis' and 6379
        },
    },
}

CELERY_BROKER_URL = 'redis://redis:6379/'  # URL for the Redis server
CELERY_RESULT_BACKEND = 'redis://redis:6379/'  # Redis backend for storing task results
# LOGGER_BOT_TOKEN = env.str("LOGGER_BOT_TOKEN")
# LOGGER_CHAT_ID = env.str("LOGGER_CHAT_ID")

# CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_HEADERS = ["*"]