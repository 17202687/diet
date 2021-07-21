"""cjb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('main/', views.main, name='main'),
    path('main/set/', views.set, name='set'),
    path('signup/', views.signup, name='signup'),
    path('main/set/user/', views.user, name='user'),
    path('main/morning/', views.morning, name='morning'),
    path('main/lunch/', views.lunch, name='lunch'),
    path('main/dinner/', views.dinner, name='dinner'),
    path('main/snack/', views.snack, name='snack'),
    path('main/set/alarm/', views.alarm, name='alarm'),
    path('main/diary/', views.diary, name='diary'),
    path('main/set/alarm/malarm/', views.malarm, name='malarm'),
    path('main/set/alarm/lalarm/', views.lalarm, name='lalarm'),
    path('main/set/alarm/dalarm/', views.dalarm, name='dalarm'),
    path('main/morning/search/', views.search, name='search'),
    path('main/lunch/search/', views.search, name='search'),
    path('main/dinner/search/', views.search, name='search'),
    
]
