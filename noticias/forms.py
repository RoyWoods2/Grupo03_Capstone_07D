# noticias/forms.py
from django import forms
from .models import Noticia


class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ["titulo", "contenido", "imagen_encabezado"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "contenido": forms.Textarea(attrs={"class": "form-control"}),
        }
