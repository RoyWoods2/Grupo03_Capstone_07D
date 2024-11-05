from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import EventoForm
from .models import Evento
from django.shortcuts import render, get_object_or_404

def detalle_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    google_maps_api_key = 'AIzaSyBIjmo2r5VEG-Lr25fPsCBlebWDDGEHaco'  # Reemplaza con tu clave de API de Google Maps
    return render(request, 'eventos/detalle_evento.html', {
        'evento': evento,
        'google_maps_api_key': google_maps_api_key
    })


def lista_eventos(request):
    eventos = Evento.objects.all().order_by('-fecha')
    return render(request, 'eventos/lista_eventos.html', {'eventos': eventos})

@login_required
def crear_evento(request):
    if not request.user.is_staff:  # Verificar si el usuario es admin
        return redirect('')

    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.autor = request.user  # Asignar al autor como el usuario autenticado
            evento.save()
            return redirect('eventos:lista_eventos')
    else:
        form = EventoForm()
    
    return render(request, 'eventos/crear_evento.html', {'form': form})
