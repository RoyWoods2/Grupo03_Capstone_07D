from django.shortcuts import render
from django.views import generic
# Create your views here.
def home(request):
    return render(request, "tekken8/home.html")