from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'home.html')


def my_view(request):
    return HttpResponse("Sobre")


def cliente(request):
    return HttpResponse("Cliente")
