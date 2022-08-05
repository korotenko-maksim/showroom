from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):
    s = "Страница категории"
    return HttpResponse(s)
