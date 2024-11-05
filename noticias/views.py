from django.shortcuts import render, redirect
from .models import Noticia
from .forms import NoticiaForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

# Vista para listar noticias
def lista_noticias(request):
    noticias = Noticia.objects.all().order_by('-fecha')
    return render(request, 'noticias/lista_noticias.html', {'noticias': noticias})

# Vista para ver el detalle de una noticia
def detalle_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    return render(request, 'noticias/detalle_noticia.html', {'noticia': noticia})

@login_required
def crear_noticia(request):
    if not request.user.is_staff and not request.groups.filter(name='Redactor').exists():
        messages.warning(request, 'Necesitas permisos de administrador o redactor para acceder a esta función.')
        return redirect('lista_noticias')
@login_required
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
            return redirect('lista_noticias')
    else:
        form = NoticiaForm()
    return render(request, 'noticias/crear_noticia.html', {'form': form})