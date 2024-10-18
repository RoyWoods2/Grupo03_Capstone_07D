from django.urls import path

from . import views

app_name = "sf6"
urlpatterns = [
    path("", views.home, name=""),

    
]
