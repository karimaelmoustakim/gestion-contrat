from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointment_list, name='appointment_list'),
    path('<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('create/', views.appointment_create, name='appointment_create'),
    path('<int:appointment_id>/edit/', views.appointment_edit, name='appointment_edit'),
    path('<int:appointment_id>/delete/', views.appointment_delete, name='appointment_delete'),
]
