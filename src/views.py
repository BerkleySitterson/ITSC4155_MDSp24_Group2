import openai
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from openai import OpenAI
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
# This file is used to set up the views/routes for the application. This is where you define functions or classes that handle HTTP requests and return responses.

# Run the following command to start the server: 'python manage.py runserver'

querySet = []

openai_api_key = 'OPEN API KEY HERE'
openai.api_key = openai_api_key

chatbot = OpenAI(api_key=openai_api_key)


def ask_openai(message):
    response = chatbot.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a music assistant, extremely knowledgeable in songs, artists, and albums."},
            {"role": "user", "content": message}
        ]
    )

    print(response)

    answer = response.choices[0].message.content.strip()

    return answer


def index(request):
    return render(request, 'index.html')


def library(request, username):
    return render(request, 'library.html', {'username': username})


def clear(request):
    querySet = []
    return render(request, 'library.html')



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Login the user
            login(request, user)
            return redirect('home', username=username)
        else:
            # Authentication failed, display error message
            messages.error(request, 'Invalid username or password. Please try again.')
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'register.html')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'register.html')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            
            if user:
                # Registration successful
                return redirect('home', username=username)
    else:
        return render(request, 'register.html')


def account(request, username):
    return render(request, 'account.html', {'username': username})


def home(request, username):
    return render(request, 'home.html', {'username': username})


def search(request, username):
    query = request.POST.get('query')
    if query is not None:
        search_history = request.session.get('search_history', [])
        search_history.append(query)
        request.session['search_history'] = search_history

        print(query)

        results = ask_openai(query)

        search_results = request.session.get('search_results', [])
        search_results.append(results)
        request.session['search_results'] = search_results

    # return redirect('home', {username=username)
    return render(request, 'home.html', {'search_results': search_results, 'username': username})


def clear_search_history(request, username):
    if request.method == 'POST':
        # Clear the search history for the given user
        request.session['search_history'] = []
        request.session['search_results'] = []
        return redirect('account', username=username)
    else:
        # Handle invalid request method
        return HttpResponse(status=405)  # Method Not Allowed


def about(request, username):
    return render(request, 'about.html', {'username': username})

def change_username(request, username):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        
        if User.objects.filter(username=new_username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'account.html', {'username': username})
        else: 
            user = User.objects.get(username=username)
            user.username = new_username
            user.save()
            return redirect('account', username=new_username)
        
    else:
        return render(request, 'account.html', {'username': username})
    
def change_password(request, username):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        
        user = User.objects.get(username=username)  
        hashed_password = make_password(new_password)
        user.password = hashed_password
        user.save()
        
        return redirect('account', username=username)       
    else:
        return render(request, 'account.html', {'username': username})
    
    
    
    
    
