# contrats/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static 
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('welcome/', views.welcome, name='welcome'),
    path('contrat/', views.contrat, name='contrat'),
    path('import_contracts/', views.import_contracts, name='import_contracts'),
     path('edit_contract/<int:contract_id>/', views.edit_contract, name='edit_contract'),
    path('delete_contract/<int:contract_id>/', views.delete_contract, name='delete_contract'),
    path('add_contract/', views.add_contract, name='add_contract'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('generate_pdf/<int:contract_id>/', views.generate_pdf, name='generate_pdf'),
    path('contract/<int:contract_id>/history/', views.contract_history, name='contract_history'),
    path('admin/all_modifications/', views.all_modifications, name='all_modifications'),
    path('calendar/', views.calendar, name='calendar'),
    path('calendar_data/', views.calendar_data, name='calendar_data'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)