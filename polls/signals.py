# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()


@receiver(post_save, sender=CustomUser)
def initialize_user(sender, instance, created, **kwargs):
    if created:
        # Aquí no necesitas acceder a `customUser`
        pass


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Si el usuario es recién creado, se ejecuta este código
        # Aquí puedes crear cualquier otra lógica para asociar algo a CustomUser si es necesario
        # Como ahora no hay UserProfile, el código puede ser modificado si necesitas asociar datos
        pass
