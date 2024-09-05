from core.settings.base import *

ALLOWED_HOSTS = ["*"]

DEBUG = True

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('localhost', 6380)], # change it to 'redis' and 6379
        },
    },
}

CELERY_BROKER_URL = 'redis://localhost:6379/'  # URL for the Redis server
CELERY_RESULT_BACKEND = 'redis://localhost:6379/'  # Redis backend for storing task results

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}