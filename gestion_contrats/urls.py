"""
URL configuration for gestion_contrats project.

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
from django.urls import path, include  # Ajoutez l'importation ici


urlpatterns = [
   path('admin/', admin.site.urls),
   path('', include('contrats.urls')),
    path('auth/', include('django.contrib.auth.urls')),
   path('auth/', include('authentication.urls')),
   path('profile/', include('profil.urls')),
   path('contact/', include('contact.urls')),
   path('notification/', include('notifications.urls')),
   path('payments/', include('payments.urls')),
   path('', include('users.urls')),
   path('app/', include('Appointment.urls')),


   



]
