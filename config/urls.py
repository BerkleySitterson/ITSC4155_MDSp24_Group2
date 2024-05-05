"""
URL configuration for SameRythymRadar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from src import views

# Everytime a new views function is added, you must also create a new urlpattern below

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.index, name='index'),
    path('user_login/', views.user_login, name='user_login'),
    path('register/', views.register, name='register'),
    path('home/<str:username>/', views.home, name='home'),
    path('search/<str:username>/', views.search, name='search'),
    path('library/<str:username>/', views.library, name='library'),
    path('library/<str:username>/', views.clear, name='clear'),
    path('account/<str:username>/', views.account, name='account'),
    path('about/<str:username>/', views.about, name='about'),
    path('account/<str:username>/clear/', views.clear_search_history, name='clear_search_history'),
    path('account/<str:username>/change_username/', views.change_username, name='change_username'),
    path('account/<str:username>/change_password/', views.change_password, name='change_password'),
]
