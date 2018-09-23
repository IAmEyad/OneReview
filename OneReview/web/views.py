import requests

from .forms import QueryForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from web.models import *
def index(request):
    # return HttpResponse("Hello, world.  You're at the polls index.")

    # render html template index.html with data in context
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def results(request):
    text_reviews = GetAmazonReviews.getTextReviews('soylent')
    cloud_image = Cloud.generate_cloud(text_reviews)
    context = {
            'text': text_reviews,
            'cloud_image': cloud_image.decode('utf-8')
    }
    return render(request, 'results.html', context=context)

def verify(request):
    return HttpResponseRedirect('https://api-sandbox.capitalone.com/oauth2/authorize?client_id=8866cf47fe3a4522850c976d63264010&grant_type=authorization_code&redirect_uri=http://127.0.0.1:8000/&scope=verify&response_type=code')

def get_query(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)

        if form.is_valid():
            
            return HttpResponseRedirect('results.html')

    else:
        form = QueryForm()
    
    return render(request, 'index.html', {'form' : form})