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
from .models import Playlist, Song, Album
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
    user = request.user
    playlists = Playlist.objects.filter(user=user)
    songs = Song.objects.filter(playlist__user=user)
    albums = Album.objects.filter(songs__playlist__user=user)

    if request.method == 'POST':
        if 'playlist_name' in request.POST:
            playlist_name = request.POST.get('playlist_name')
            playlist = Playlist.objects.create(name=playlist_name, user=user)
            return redirect('library', username=username)

        elif 'song_title' in request.POST:
            song_title = request.POST.get('song_title')
            artist = request.POST.get('artist')
            album_title = request.POST.get('album_title')
            playlist_id = request.POST.get('playlist')

            if album_title:
                album, _ = Album.objects.get_or_create(title=album_title, artist=artist)
            else:
                album = None

            song = Song.objects.create(title=song_title, artist=artist, album=album)

            if playlist_id == 'all':
                song.playlist.set(Playlist.objects.filter(user=user))
            else:
                playlist = Playlist.objects.get(id=playlist_id, user=user)
                song.playlist.add(playlist)

            return redirect('library', username=username)

    selected_playlist = None
    selected_playlist_albums = []  # Initialize with an empty list

    if 'playlist' in request.GET:
        playlist_id = request.GET.get('playlist')
        if playlist_id != 'all':
            selected_playlist = Playlist.objects.get(id=playlist_id, user=user)
            selected_playlist_songs = selected_playlist.songs.all()
            selected_playlist_albums = Album.objects.filter(songs__in=selected_playlist_songs).distinct()
            if not selected_playlist_albums:
                selected_playlist_albums = []  # Clear the queryset if no albums found

    context = {
        'username': username,
        'playlists': playlists,
        'songs': songs,
        'albums': albums,
        'selected_playlist': selected_playlist,
        'selected_playlist_albums': selected_playlist_albums,
    }

    return render(request, 'library.html', context)

def delete_playlist(request, username, playlist_id):
    if request.method == 'POST':
        user = request.user
        playlist = Playlist.objects.filter(id=playlist_id, user=user)
        if playlist.exists():
            playlist.delete()
    return redirect('library', username=username)

def delete_song(request, username, song_id):
    if request.method == 'POST':
        song = Song.objects.filter(id=song_id)
        if song.exists():
            song.delete()
    return redirect('library', username=username)

def delete_album(request, username, album_id):
    if request.method == 'POST':
        album = Album.objects.filter(id=album_id)
        if album.exists():
            album.delete()
    return redirect('library', username=username)

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
    
    
    
    
    
