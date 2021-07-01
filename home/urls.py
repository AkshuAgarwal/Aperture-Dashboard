from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('home/', views.index, name='home'),
    path('login/', views.login, name='login'),
    path('callback/', views.callback, name='callback'),
    path('dashboard/', include('dashboard.urls')),
    path('logout/', views.logout, name='logout'),
    path('cookiedisabled/', views.cookiedisabled, name='cookie_disabled'),
    path('noscript/', views.noscript, name='noscript'),
]
