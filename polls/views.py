from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
from django.conf import settings
from .forms import CustomUserCreationForm



from .models import Choice, Question

# Create your views here.
from django.shortcuts import render, redirect
from .forms import ComentarioForm
from .models import Comentario
from django.contrib.auth.decorators import login_required

@login_required (login_url="/login")
def comentarios_vista(request):
    # Manejar el envío de un comentario o respuesta
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            # Verificar si el comentario es una respuesta a otro comentario
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comentario.parent = get_object_or_404(Comentario, id=parent_id)
            comentario.save()
            return redirect('/prueba')
    else:
        form = ComentarioForm()

    # Mostrar comentarios principales (sin parent)
    comentarios = Comentario.objects.filter(parent__isnull=True).order_by('-fecha_publicacion')

    return render(request, 'polls/prueba.html', {'form': form, 'comentarios': comentarios})




# Supón que tienes una URL de API y un token de acceso para Behold
API_URL = "https://api.behold.com/v1/data"
API_TOKEN = "tu_api_token_aqui"

def get_behold_data():
    headers = {
        'Authorization': f'Bearer {API_TOKEN}'
    }
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()  # Devuelve los datos en formato JSON
    else:
        return {}  # En caso de error, devuelve un diccionario vacío

def behold_data_view(request):
    data = get_behold_data()
    return render(request, 'behold_data.html', {'data': data})
def registro_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Recarga el perfil para capturar los datos "nick"
            user.userprofile.nick = form.cleaned_data.get('nick')
            user.userprofile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Cuenta creada para {username}")
            login(request, user)
            return redirect('/')  # Cambia 'home' por la URL a la que quieres redirigir
    else:
        form = CustomUserCreationForm()
    return render(request, 'polls/registro.html', {'form': form})

# Vista de cierre de sesión
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('/')


# Vista de inicio de sesión
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/juegos')  # Redirigir al dashboard de administrador
            else:
                return redirect('/')  # Redirigir al dashboard de usuario normal
        else:
            messages.error(request, 'Credenciales inválidas. Por favor intenta nuevamente.')
    
    return render(request, 'polls/login.html')




class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]
    

    
    


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def juegos(request):
    return render(request, "polls/juegos.html")
def base(request):
    return render(request, "polls/base.html")

def prueba(request):
    return render(request, "polls/prueba.html")

    
def index(request):
   
    return render(request, "polls/index.html")


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})