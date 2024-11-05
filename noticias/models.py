from django.db import models
from django.contrib.auth.models import User

class Noticia(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    contenido = models.TextField()
    imagen_encabezado = models.ImageField(upload_to='noticias/', blank=True, null=True)  # Nuevo campo para la imagen

    def __str__(self):
        return self.titulo