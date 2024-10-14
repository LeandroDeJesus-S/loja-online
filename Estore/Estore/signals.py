import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from dotenv import load_dotenv


@receiver(post_migrate, dispatch_uid='base_superuser_dispatch')
def create_base_superuser(sender, **kwargs):
    """creates a initial super user"""
    load_dotenv(
        settings.BASE_DIR.parent / "dotenv_files" / ".env",
        override=True,
    )
    User = get_user_model()
    username = os.environ["ADMIN_USERNAME"]
    email = os.environ["ADMIN_EMAIL"]
    password = os.environ["ADMIN_PASSWORD"]

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
