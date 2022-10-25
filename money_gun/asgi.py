"""
ASGI config for money_gun project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Create your ASGI here.


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'money_gun.settings')

application = get_asgi_application()
