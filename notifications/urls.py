# contrats/urls.py
from django.urls import path
from . import views

urlpatterns = [
     path('', views.notifications, name='notifications'),
    path('mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('send_expiration_notifications/', views.send_expiration_notifications, name='send_expiration_notifications'),
     path('check_and_notify_expiring_contracts/', views.check_and_notify_expiring_contracts, name='check_and_notify_expiring_contracts'),
     path('notifications/delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('notifications/read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
  
      
]