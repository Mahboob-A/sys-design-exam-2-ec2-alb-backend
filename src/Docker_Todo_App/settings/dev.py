from datetime import timedelta 
from .base import * 
from .base import env


# ################# Security

SECRET_KEY = env.str("SECRET_KEY")
DJANGO_LOCAL_PORT = env.str("DJANGO_LOCAL_PORT")
DJANGO_DOCKER_PORT = env.str("DJANGO_DOCKER_PORT")
ADMIN_URL = env("ADMIN_URL")
 
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]

CSRF_TRUSTED_ORIGINS = [
    f"http://127.0.0.1:{DJANGO_LOCAL_PORT}", # 8000
    f"http://127.0.0.1:{DJANGO_DOCKER_PORT}", # 8080
]

CORS_ALLOWED_ORIGINS = [
    f"http://127.0.0.1:{DJANGO_LOCAL_PORT}", 
    f"http://127.0.0.1:{DJANGO_DOCKER_PORT}", 
]


############################ ADDED SETTINGS ###############################

# ################# Static and Media

STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / "staticfiles")
MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR / "mediafiles")


