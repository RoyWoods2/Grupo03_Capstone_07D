from django.shortcuts import render, redirect
from .models import Noticia
from polls.models import Comentario
from .forms import NoticiaForm
from polls.forms import ComentarioForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

# Vista para listar noticias
def lista_noticias(request):
    noticias = Noticia.objects.all().order_by('-fecha')
    return render(request, 'noticias/lista_noticias.html', {'noticias': noticias})

# Vista para ver el detalle de una noticia
def detalle_noticia(request, slug):
    noticia = get_object_or_404(Noticia, slug=slug)
    comentarios = noticia.comentarios.filter(respuesta_a=None)

        # Gestionar la creación de un nuevo comentario
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.noticia = noticia
            comentario.usuario = request.user
            comentario.save()
            respuesta_id = request.POST.get("respuesta_id")
            if respuesta_id:
                comentario.respuesta_a_id = respuesta_id
            comentario.save()
            return redirect('noticias:detalle_noticia', slug=noticia.slug)
    else:
        form = ComentarioForm()
        
    return render(request, 'noticias/detalle_noticia.html', {'noticia': noticia , 'comentarios': comentarios, 'form': form})


def es_redactor_o_admin(user):
    return user.is_staff or user.groups.filter(name='Redactor').exists()

@login_required
@user_passes_test(es_redactor_o_admin, login_url='acceso_denegado')
def crear_noticia(request):
    if not request.user.is_staff and not request.groups.filter(name='Redactor').exists():
        messages.warning(request, 'Necesitas permisos de administrador o redactor para acceder a esta función.')
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.autor = request.user
            noticia.fecha = timezone.now()
            noticia.save()
            return redirect('noticias:lista_noticias')
    else:
        form = NoticiaForm()
    return render(request, 'noticias/crear_noticia.html', {'form': form})


# Vista de acceso denegado
def acceso_denegado(request):
    return render(request, 'noticias/acceso_denegado.html')