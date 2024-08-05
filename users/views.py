from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from contrats.models import Contract, Notification  # Assurez-vous d'importer les modèles depuis votre application `contrats`

@login_required
def user_dashboard(request):
    contracts = Contract.objects.filter(user=request.user)
    notifications = Notification.objects.filter(user=request.user, read=False)
    
    # Calcul des statistiques
    total_contracts = contracts.count()
    active_contracts = contracts.filter(status='active').count()
    near_expiry_contracts = contracts.filter(status='near_expiry').count()
    expired_contracts = contracts.filter(status='expired').count()
    
    context = {
        'total_contracts': total_contracts,
        'active_contracts': active_contracts,
        'near_expiry_contracts': near_expiry_contracts,
        'expired_contracts': expired_contracts,
        'notifications': notifications,
    }
    
    return render(request, 'user_dashboard.html', context)
