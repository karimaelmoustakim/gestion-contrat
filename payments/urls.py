from django.urls import path
from . import views

urlpatterns = [
    path('contract/<int:contract_id>/payments/', views.payment_list, name='payment_list'),
    path('contract/<int:contract_id>/payments/add/', views.add_payment, name='add_payment'),
    path('payments/<int:payment_id>/', views.payment_detail, name='payment_detail'),
    path('send_payment_reminders/', views.send_payment_reminders, name='send_payment_reminders'),
    path('payments/dashboard/', views.payment_dashboard, name='payment_dashboard'),
    path('payment/<int:payment_id>/edit/', views.edit_payment, name='edit_payment'),
    path('payment/<int:payment_id>/delete/', views.delete_payment, name='delete_payment'),



]
