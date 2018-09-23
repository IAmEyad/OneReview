import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

def index(request):
    # return HttpResponse("Hello, world.  You're at the polls index.")

    # render html template index.html with data in context
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def results(request):
    return render(request, 'results.html')

def verify(request):
    return HttpResponseRedirect('https://api-sandbox.capitalone.com/oauth2/authorize?client_id=8866cf47fe3a4522850c976d63264010&grant_type=authorization_code&redirect_uri=http://127.0.0.1:8000/&scope=verify&response_type=code')
