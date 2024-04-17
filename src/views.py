from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from .models import User

# This file is used to set up the views/routes for the application. This is where you define functions or classes that handle HTTP requests and return responses.

# Run the following command to start the server: 'python manage.py runserver'

querySet = []

def index(request):
    return render(request, 'index.html')

def library(request, username):
    return render(request, 'library.html', {'username': username})

def clear(request):
    querySet = []
    return render(request, 'library.html')

def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username is not None and password is not None:
        user = User.objects.filter(username=username, password=password)
        if user.exists():
            return redirect('home', username=username)        
    else:
        return render(request, 'index.html')
    
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email is not None and password is not None and username is not None:
            user = User(username=username, email=email, password=password)
            user.save()
            return redirect('home', {'username': username})
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'register.html')
    
def account(request, username):
    return render(request, 'account.html', {'username': username})

def home(request, username):
    return render(request, 'home.html', {'username': username})

def search(request, username):
    query = request.POST.get('query')
    if query is not None:
        querySet.append(query)
    return render(request, 'home.html', {'querySet': querySet, 'username': username})

def about(request, username):
    return render(request, 'about.html', {'username': username})
