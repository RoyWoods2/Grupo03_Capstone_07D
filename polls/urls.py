from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path('', views.index ,name=''),
    path("juegos",views.juegos, name="juegos"),
    path("base",views.base, name="base"),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('registro', views.registro_view, name='registro'),
    path('prueba', views.comentarios_vista, name='prueba'),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]