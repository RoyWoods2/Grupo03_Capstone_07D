from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Comentario,UserProfile,CustomUser
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
    class Meta:
        model = UserProfile
        fields = ['nick', 'name', 'email', 'avatar', 'juegos_competencia', 'user_type']
        widgets = {
            'nick': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'juegos_competencia': forms.Textarea(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
        }
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe tu comentario o respuesta...'}),
        }

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


class CustomUserCreationForm(UserCreationForm):
    nick = forms.CharField(max_length=30, required=True, label="Nickname")
    name = forms.CharField(max_length=100, required=True, label="Full Name")
    email = forms.EmailField(max_length=100, required=True, label="Email")

    class Meta:
        model = CustomUser
        fields = ("username", "password1", "password2", "nick", "name", "email")

    def save(self, commit=True):
        user = super().save(commit=commit)
        user_profile = UserProfile.objects.create(
            user=user,
            nick=self.cleaned_data['nick'],
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            avatar=self.cleaned_data.get('avatar')
        )
        return user