"""
ASGI config for Docker_Todo_App project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# NOTE: Currently .dev settings is being used as production environment is not needed.  
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Docker_Todo_App.settings.dev")

application = get_asgi_application()
