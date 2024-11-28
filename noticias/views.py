from django.shortcuts import render, redirect
from .models import Noticia
from polls.models import Comentario
from .forms import NoticiaForm
from polls.forms import ComentarioForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect


@login_required
def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id, usuario=request.user)
    if request.method == "POST":
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect("detalle_noticia", slug=comentario.noticia.slug)
    else:
        form = ComentarioForm(instance=comentario)
    return render(request, "editar_comentario.html", {"form": form})


@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id, usuario=request.user)
    if request.method == "POST":
        comentario.delete()
        return redirect("detalle_noticia", slug=comentario.noticia.slug)
    return render(request, "confirmar_eliminar.html", {"comentario": comentario})


# Vista para listar noticias
def lista_noticias(request):
    noticias = Noticia.objects.all().order_by("-fecha")
    return render(request, "noticias/lista_noticias.html", {"noticias": noticias})


# Vista para ver el detalle de una noticia
def detalle_noticia(request, slug):
    noticia = get_object_or_404(Noticia, slug=slug)
    comentarios = Comentario.objects.filter(
        noticia=noticia, respuesta_a=None
    )  # Comentarios principales

    if request.method == "POST":
        respuesta_a_id = request.POST.get(
            "comentario_padre_id"
        )  # ID del comentario al que se responde
        contenido = request.POST.get("contenido")

        if contenido:
            nuevo_comentario = Comentario(
                noticia=noticia,
                usuario=request.user,
                contenido=contenido,
                respuesta_a_id=(
                    respuesta_a_id if respuesta_a_id else None
                ),  # Relación con el comentario padre
            )
            nuevo_comentario.save()
            return redirect("noticias:detalle_noticia", slug=slug)

    return render(
        request,
        "noticias/detalle_noticia.html",
        {
            "noticia": noticia,
            "comentarios": comentarios,
            "form": ComentarioForm(),
        },
    )


def es_redactor_o_admin(user):
    return user.is_staff or user.groups.filter(name="Redactor").exists()


@login_required
def crear_noticia(request):

    if request.method == "POST":
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.autor = request.user
            noticia.fecha = timezone.now()
            noticia.save()
            return redirect("noticias:lista_noticias")
    else:
        form = NoticiaForm()
    return render(request, "noticias/crear_noticia.html", {"form": form})


# Vista de acceso denegado
def acceso_denegado(request):
    return render(request, "noticias/acceso_denegado.html")
