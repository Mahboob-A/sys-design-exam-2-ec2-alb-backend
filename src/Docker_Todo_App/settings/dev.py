from datetime import timedelta 
from .base import * 
from .base import env


# ################# Security

SECRET_KEY = env.str("SECRET_KEY")
ADMIN_URL = env("ADMIN_URL")

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",  
    "http://127.0.0.1:8080",  
    "http://127.0.0.1:3000",
]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:3000",
]


############################ ADDED SETTINGS ###############################

# ################# Static and Media

STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / "staticfiles")
MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR / "mediafiles")
