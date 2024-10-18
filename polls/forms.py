from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe tu comentario o respuesta...'}),
        }



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. Ingresa un email válido.", error_messages={
        'required': 'El campo de email es obligatorio.',
        'invalid': 'Por favor, ingresa un email válido.'})
    nombre = forms.CharField(max_length=30, required=True, help_text="Requerido. Ingrese su nombre completo." ,error_messages={
        'required': 'El campo de hombre es obligatorio.',
        'invalid': 'Por favor, ingresa un email válido.'})
    apellido = forms.CharField(max_length=30, required=True, help_text="Requerido. Ingrese su apellido.",error_messages={
        'required': 'El campo de apellido es obligatorio.',
        'invalid': 'Por favor, ingresa un email válido.'})
    nick = forms.CharField(max_length=30, required=True, help_text="Requerido. Ingrese su apodo o nick.",error_messages={
        'required': 'El campo de nick es obligatorio.',
        'invalid': 'Por favor, ingresa un email válido.'})

    class Meta:
        model = User
        fields = ['username', 'nick', 'nombre', 'apellido', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.nombre = self.cleaned_data['nombre']
        user.apellido = self.cleaned_data['apellido']
        
        # No tenemos un campo "nick" en el modelo User por defecto
        # Si necesitas un campo adicional como "nick", puedes usar un perfil de usuario.
        
        if commit:
            user.save()
        return user
