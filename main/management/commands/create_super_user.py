import os

from django.core.management.base import BaseCommand

from main.models import User


class Command(BaseCommand):
    args = ''
    help = 'Create Super User'

    def handle(self, *args, **options):
        email = os.environ['ADMIN_EMAIL']
        password = os.environ['ADMIN_PASSWORD']

        user = User.objects.filter(email=email).first()
        if not user:
            User.objects.create_superuser(email=email, password=password)
