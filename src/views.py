from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect

# This file is used to set up the views/routes for the application. This is where you define functions or classes that handle HTTP requests and return responses.

# Run the following command to start the server: 'python manage.py runserver'

def index(request):
    return render(request, 'index.html')

def library(request):
    return render(request, 'library.html')

def login(request):
    # Add logic to check username and password in database
    
    username = request.POST.get('username')
    
    if (True):
        return redirect('home', username=username)
    else:
        return render(request, 'index.html')

def home(request, username):
    return render(request, 'home.html', {'username': username})

def search(request, username):
    query = request.POST.get('query')
    return render(request, 'home.html', {'username': username, 'query': query})