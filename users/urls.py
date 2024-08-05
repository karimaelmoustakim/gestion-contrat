from django.urls import path
from . import views

urlpatterns = [
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
]
