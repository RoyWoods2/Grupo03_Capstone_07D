from django import forms
from .models import Evento,TorneoComunitario


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = [
            "titulo",
            "fecha",
            "contenido",
            "autor",
            "imagen",
            "direccion",
            "premio_primer_lugar",
            "premio_segundo_lugar",
            "premio_tercer_lugar",
        ]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "fecha": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "contenido": forms.Textarea(attrs={"class": "form-control"}),
            "autor": forms.Select(attrs={"class": "form-control"}),
            "imagen": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
            "premio_primer_lugar": forms.NumberInput(attrs={"class": "form-control"}),
            "premio_segundo_lugar": forms.NumberInput(attrs={"class": "form-control"}),
            "premio_tercer_lugar": forms.NumberInput(attrs={"class": "form-control"}),
        }

class TorneoComunitarioForm(forms.ModelForm):
    class Meta:
        model = TorneoComunitario
        fields = ['titulo', 'fecha', 'tipo_torneo', 'descripcion', 'imagen', 'direccion']
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),  # Sin "display: none"
        }