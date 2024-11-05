from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_noticias, name='lista_noticias'),
    path('<int:noticia_id>/', views.detalle_noticia, name='detalle_noticia'),
    path('crear/', views.crear_noticia, name='crear_noticia'),  # Nueva URL para crear noticias

]