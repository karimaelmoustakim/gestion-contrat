from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Payment
from contrats.models import Contract
from .forms import PaymentForm 
from django.db.models import Sum, Count
from django.urls import reverse



@login_required
def payment_list(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    payments = contract.payments.all()
    return render(request, 'payment_list.html', {'contract': contract, 'payments': payments})

@login_required
def add_payment(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.contract = contract
            payment.created_by = request.user
            payment.save()
            return redirect('payment_list', contract_id=contract.id)
    else:
        form = PaymentForm()
    return render(request, 'add_payment.html', {'form': form, 'contract': contract})

    
@login_required
def edit_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('payment_list', contract_id=payment.contract.id)
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'edit_payment.html', {'form': form, 'payment': payment})


@login_required
def delete_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    contract_id = payment.contract.id
    payment.delete()
    return redirect(reverse('payment_list', args=[contract_id]))

@login_required
def payment_detail(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'payment_detail.html', {'payment': payment})

@login_required
def send_payment_reminders(request):
    overdue_payments = Payment.objects.filter(payment_date__lt=timezone.now(), status='pending')
    for payment in overdue_payments:
        send_mail(
            'Rappel de Paiement en Retard',
            f'Le paiement pour le contrat {payment.contract.contract_number} de {payment.amount} est en retard.',
            settings.DEFAULT_FROM_EMAIL,
            [payment.contract.client_mail],
            fail_silently=False,
        )
    return HttpResponse('Rappels envoyés avec succès.')


@login_required
def payment_dashboard(request):
    total_payments = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    completed_payments = Payment.objects.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
    pending_payments = Payment.objects.filter(status='pending').aggregate(Sum('amount'))['amount__sum'] or 0

    payment_status_counts = Payment.objects.values('status').annotate(count=Count('status'))
    payment_statuses = {item['status']: item['count'] for item in payment_status_counts}

    return render(request, 'payment_dashboard.html', {
        'total_payments': total_payments,
        'completed_payments': completed_payments,
        'pending_payments': pending_payments,
        'payment_statuses': payment_statuses,
    })


