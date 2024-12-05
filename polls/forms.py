from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Comentario, CustomUser, Juego, RoleChangeRequest, Estrategia,Recurso,Moderacion
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
import re

class ModeracionForm(forms.ModelForm):
    class Meta:
        model = Moderacion
        fields = ['strikes', 'comentarios_bloqueados', 'torneos_bloqueados']
class RecursoForm(forms.ModelForm):
    class Meta:
        model = Recurso
        fields = ['personaje', 'descripcion', 'enlace_video', 'categoria']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "nick",
            "email",
            "avatar",
            "juegos_competencia",
            "user_type",
        ]


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "nick",
            "email",
            "avatar",
            "juegos_competencia",
            "user_type",
        ]


class UserProfileForm(forms.ModelForm):
    juegos_competencia = forms.ModelMultipleChoiceField(
        queryset=Juego.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Juegos en los que compites",
    )
    def clean_twitch_stream(self):
        twitch_url = self.cleaned_data.get('twitch_stream')
        if twitch_url and not twitch_url.startswith("https://www.twitch.tv/"):
            raise forms.ValidationError("El enlace debe comenzar con 'https://www.twitch.tv/'.")
        return twitch_url

    def clean_youtube_channel(self):
        youtube_url = self.cleaned_data.get('youtube_channel')
        if youtube_url and not ("youtube.com" in youtube_url):
            raise forms.ValidationError("Ingrese una URL válida de YouTube.")
        return youtube_url
    def clean_musica_fondo(self):
        musica_fondo = self.cleaned_data.get('musica_fondo')
        if musica_fondo and not musica_fondo.startswith("https://soundcloud.com/"):
            raise forms.ValidationError("La URL debe ser un enlace válido de SoundCloud.")
        return musica_fondo
    class Meta:
        model = CustomUser
        fields = ['avatar', 'name', 'email', 'tema_perfil', 'musica_fondo', 'imagen_fondo']
        widgets = {
            'tema_perfil': forms.Select(attrs={'class': 'form-control'}),
            'musica_fondo': forms.TextInput(attrs={'placeholder': 'URL de música de fondo', 'class': 'form-control'}),
            'imagen_fondo': forms.ClearableFileInput(attrs={'class': 'form-control'}),

        }

    def clean_nick(self):
        nick = self.cleaned_data["nick"]
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(nick=nick).exists():
            raise forms.ValidationError("Este nickname ya está en uso.")
        return nick


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ["contenido"]
        widgets = {
            "contenido": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Escribe tu comentario o respuesta...",
                }
            ),
        }


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ingresa tu usuario"}
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Ingresa tu contraseña"}
        ),
    )


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, label="Nombre de usuario")
    email = forms.EmailField(max_length=100, required=True, label="Email")

    class Meta:
        model = CustomUser
        fields = ("username", "password1", "password2", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        # Asignar automáticamente el username como nick
        user.nick = user.username
        user.name = self.cleaned_data.get(
            "name", ""
        )  # Si no se proporciona, queda vacío
        user.avatar = self.cleaned_data.get("avatar", "polls/css/images/default.png")

        if commit:
            user.save()
        return user


class RoleChangeRequestForm(forms.ModelForm):
    class Meta:
        model = RoleChangeRequest
        fields = ["rol_solicitado", "mensaje"]
        labels = {
            "rol_solicitado": "Rol deseado",
            "mensaje": "Motivo o mensaje al administrador",
        }


class EstrategiaForm(forms.ModelForm):
    class Meta:
        model = Estrategia
        fields = [
            "tacticas_generales",
            "posicionamiento_en_el_equipo",
            "block_string",
            "oki",
            "tips_y_trucos",
            "luchando_en_contra",
        ]
        widgets = {
            "tacticas_generales": forms.Textarea(attrs={"rows": 4, "cols": 50}),
            "posicionamiento_en_el_equipo": forms.Textarea(
                attrs={"rows": 4, "cols": 50}
            ),
            "block_string": forms.Textarea(attrs={"rows": 4, "cols": 50}),
            "oki": forms.Textarea(attrs={"rows": 4, "cols": 50}),
            "tips_y_trucos": forms.Textarea(attrs={"rows": 4, "cols": 50}),
            "luchando_en_contra": forms.Textarea(attrs={"rows": 4, "cols": 50}),
        }
