from pathlib import Path
from environ import Env 

BASE_DIR = Path(__file__).resolve().parent.parent.parent 
APP_DIR = BASE_DIR / "core_apps"

# Env Setup 
env = Env()
ENVIRONMENT_TYPE = env("ENVIRONMENT_TYPE", default=".dev")
env.read_env(Path(str(BASE_DIR)) / f".envs/{ENVIRONMENT_TYPE}/.django")
env.read_env(Path(str(BASE_DIR)) / f".envs/{ENVIRONMENT_TYPE}/.postgres")


DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTH_APPS = [
    "rest_framework",
    "drf_yasg",
    "corsheaders",
]

LOCAL_APPS = [
    "core_apps.common",
    "core_apps.todo",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTH_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Docker_Todo_App.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Docker_Todo_App.wsgi.application"

# NOTE: Local Database for Test 
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Docker Database
# DATABASES = {"default": env.db("DATABASE_URL")}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]



LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
