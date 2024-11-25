from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Comentario,CustomUser,Juego,RoleChangeRequest
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'nick', 'email', 'avatar', 'juegos_competencia', 'user_type']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'nick', 'email', 'avatar', 'juegos_competencia', 'user_type']
        
        

class UserProfileForm(forms.ModelForm):
    juegos_competencia = forms.ModelMultipleChoiceField(
        queryset=Juego.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Juegos en los que compites"
    )

    class Meta:
        model = CustomUser
        fields = ['nick','avatar', 'name', 'juegos_competencia']
    def clean_nick(self):
        nick = self.cleaned_data['nick']
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(nick=nick).exists():
            raise forms.ValidationError("Este nickname ya está en uso.")
        return nick
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe tu comentario o respuesta...'}),
        }

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu usuario'}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu contraseña'}),
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
        user.name = self.cleaned_data.get('name', '')  # Si no se proporciona, queda vacío
        user.avatar = self.cleaned_data.get('avatar', 'polls/css/images/default.png')

        if commit:
            user.save()
        return user
    
    
class RoleChangeRequestForm(forms.ModelForm):
    class Meta:
        model = RoleChangeRequest
        fields = ['rol_solicitado', 'mensaje']
        labels = {
            'rol_solicitado': 'Rol deseado',
            'mensaje': 'Motivo o mensaje al administrador',
        }