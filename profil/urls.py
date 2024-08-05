# contrats/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('profil/', views.profil, name='profil'),   
    path('update_profile/', views.update_profile, name='update_profile'),
]