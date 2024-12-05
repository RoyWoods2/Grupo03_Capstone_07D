from django.core.management.base import BaseCommand
from polls.models import CustomUser
import random
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Genera usuarios de prueba automáticamente'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cantidad', type=int, default=10, help='Número de usuarios a crear'
        )

    def handle(self, *args, **kwargs):
        cantidad = kwargs['cantidad']
        for _ in range(cantidad):
            username = fake.user_name()
            nick = fake.unique.first_name()
            email = fake.unique.email()
            user_type = random.choice(["normal", "admin", "redactor", "organizador"])
            
            user = CustomUser.objects.create_user(
                username=username,
                password='password123',  # Cambiar si necesitas contraseñas específicas
                email=email,
                user_type=user_type,
                puntos=random.randint(0, 100)
            )
            user.save()
            self.stdout.write(f'Usuario creado: {user.username} ({user.nick})')
