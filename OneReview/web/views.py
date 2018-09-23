import requests
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    # return HttpResponse("Hello, world.  You're at the polls index.")

    # render html template index.html with data in context
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def results(request):
    return render(request, 'results.html')
