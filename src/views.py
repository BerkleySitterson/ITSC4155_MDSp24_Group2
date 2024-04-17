from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .models import User

# This file is used to set up the views/routes for the application. This is where you define functions or classes that handle HTTP requests and return responses.

# Run the following command to start the server: 'python manage.py runserver'

def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()  # Use CustomUser manager
        if user is not None and user.check_password(password):
            login(request, user)
            return redirect('home')  # Replace 'home' with your desired URL name
        else:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'index.html', {'error_message': 'Invalid registration form.'})
    else:
        return render(request, 'index.html')
    

def home(request):
    return render(request, 'home.html')

def account(request):
    return render(request, 'account.html')
    
def library(request):
    return render(request, 'library.html')

def about(request):
    return render(request, 'about.html')