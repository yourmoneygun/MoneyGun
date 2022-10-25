"""
WSGI config for money_gun project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Create your WSGI here.


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'money_gun.settings')

application = get_wsgi_application()
