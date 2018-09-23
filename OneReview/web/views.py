import requests
from django.http import HttpResponse
from django.shortcuts import render
from . import models

def index(request):
    return render(request, 'index.html')

def verify(request):
    if request.method == 'POST':
        url = 'https://api-sandbox.capitalone.com/oauth2/token'
        r = requests.post(url, data =[('client_id',models.User.client_id), 'client_secret' = [models.User.client_secret], 'grant_type' = ['client_credentials']})
    return render(request, 'login.html')