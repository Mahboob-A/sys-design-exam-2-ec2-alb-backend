from datetime import timedelta 
from .base import * 
from .base import env


# ################# Security

SECRET_KEY = env.str("SECRET_KEY")
ADMIN_URL = env("ADMIN_URL")

DJANGO_LOCAL_PORT = env("DJANGO_LOCAL_PORT")  # 8000
DJANGO_DOCKER_PORT = env("DJANGO_DOCKER_PORT") # 9090

DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:9090",
]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:9090",
]


############################ ADDED SETTINGS ###############################

# ################# Static and Media

STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / "staticfiles")
MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR / "mediafiles")
