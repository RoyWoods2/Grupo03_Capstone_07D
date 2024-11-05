from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Evento(models.Model):
    titulo = models.CharField(max_length=255)
    fecha = models.DateField()
    contenido = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='eventos/', null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)  # Nueva variable de dirección

    def __str__(self):
        return self.titulo
