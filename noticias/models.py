from django.db import models
from django.contrib.auth.models import User
from django.conf import settings  # Importa settings para usar AUTH_USER_MODEL
from django.utils.text import slugify


class Noticia(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    contenido = models.TextField()
    imagen_encabezado = models.ImageField(upload_to='noticias/', blank=True, null=True)  # Nuevo campo para la imagen

 
    def save(self, *args, **kwargs):
        # Genera el slug basado en el título
        if not self.slug:
            self.slug = slugify(self.titulo.replace(" ", "_"))
        super(Noticia, self).save(*args, **kwargs)

    def __str__(self):
        return self.titul