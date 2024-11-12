from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.conf import settings  # Importa settings para usar AUTH_USER_MODEL

# Create your models here.
class Evento(models.Model):
    titulo = models.CharField(max_length=255)
    fecha = models.DateField()
    contenido = models.TextField()
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    imagen = models.ImageField(upload_to='eventos/', null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)  # Nueva variable de dirección

    def __str__(self):
        return self.titulo
