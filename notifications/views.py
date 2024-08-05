from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user, contract__status='near_expiry').order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.read = True
    notification.save()
    return redirect('notifications')

@login_required
def check_and_notify_expiring_contracts(request):
    contracts = Contract.objects.filter(expiration_date__lte=timezone.now() + timedelta(days=7), status='active')
    for contract in contracts:
        contract.status = 'near_expiry'
        contract.save()
        # Vérifier si une notification existe déjà pour ce contrat
        if not Notification.objects.filter(contract=contract).exists():
            Notification.objects.create(
                user=contract.user,
                contract=contract,
                message=f"Le contrat numéro {contract.contract_number} pour {contract.client_name} expire bientôt.",
                priority='high'  # Définir la priorité ici
            )
            send_mail(
                'Notification de contrat proche d\'expiration',
                f'Le contrat numéro {contract.contract_number} pour {contract.client_name} expire bientôt.',
                settings.DEFAULT_FROM_EMAIL,
                ['karimaelmoustakim2002@gmail.com'],
                fail_silently=False,
            )
    return redirect('notifications')



def send_expiration_notifications(request):
    contracts = Contract.objects.filter(expiration_date__lte=timezone.now() + timedelta(days=7))
    for contract in contracts:
        send_mail(
            'Notification de contrat proche d\'expiration',
            f'Le contrat numéro {contract.contract_number} est proche d\'expirer le {contract.expiration_date}.',
            'karimaelmoustakim2002@gmail.com',  # Remplacez par votre adresse email
            ['karimaelmoustakim2002@gmail.com'],  # Adresse email de destination
            fail_silently=False,
        )
    return HttpResponse('Notifications envoyées avec succès.')

@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.delete()
    return redirect('notifications')
