import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Contract
from .models import Notification
from django.contrib.auth.models import User
from .forms import ContractForm
from django.db.models import Count
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import ContractHistory 
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q





@login_required
def import_contracts(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)

        # Convert date fields to string in ISO format
        df['Expiration Date'] = pd.to_datetime(df['Expiration Date'], errors='coerce').dt.strftime('%Y-%m-%d')
        df['Birthday Date'] = pd.to_datetime(df['Birthday Date'], errors='coerce').dt.strftime('%Y-%m-%d')

        for _, row in df.iterrows():
            # Ensure dates are converted to strings if not already
            expiration_date = str(row['Expiration Date']) if pd.notnull(row['Expiration Date']) else None
            birthday_date = str(row['Birthday Date']) if pd.notnull(row['Birthday Date']) else None

            Contract.objects.create(
                user=request.user,
                contract_number=row['Contract Number'],
                client_name=row['Client Name'],
                client_mail=row['Client Mail'],
                expiration_date=expiration_date,
                product=row['Product'],
                contract_type=row['Contract Type'],
                purchase_price=row['Purchase Price'],
                selling_price=row['Selling Price'],
                remaining_month=row['Remaining Months'],
                birthday_date=birthday_date,
                status=row.get('Status', 'active')  # Default to 'active' if 'Status' is not present
            )

        return redirect('contrat')

    return render(request, 'import_contracts.html')

@login_required
def contrat(request):
    query = request.GET.get('q')
    if request.user.is_superuser:
        contracts = Contract.objects.all()
    else:
        contracts = Contract.objects.filter(user=request.user)
    
    if query:
        contracts = contracts.filter(Q(contract_number__icontains=query) | Q(client_name__icontains=query))

    paginator = Paginator(contracts, 3)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'contrat.html', {'page_obj': page_obj, 'query': query})

@login_required
def edit_contract(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES, instance=contract)
        if form.is_valid():
            old_contract = Contract.objects.get(id=contract_id)  # Get old contract data for comparison
            contract = form.save(commit=False)
            change_description = ""

            # Compare old and new values, and create change description
            for field in form.changed_data:
                old_value = getattr(old_contract, field)
                new_value = getattr(contract, field)
                change_description += f"{field} changed from {old_value} to {new_value}. "

            # Save the contract and create a history record
            contract.save()
            if change_description:
                ContractHistory.objects.create(
                    contract=contract,
                    user=request.user,
                    change_description=change_description
                )
            
            if contract.status == 'near_expiry':
                notification, created = Notification.objects.get_or_create(
                    user=contract.user,
                    contract=contract,
                    defaults={'message': f"Le contrat numéro {contract.contract_number} pour {contract.client_name} expire bientôt."}
                )
                if not created:
                    notification.message = f"Le contrat numéro {contract.contract_number} pour {contract.client_name} expire bientôt."
                    notification.save()
            else:
                Notification.objects.filter(contract=contract).delete()

            return redirect('contrat')
    else:
        form = ContractForm(instance=contract)
    return render(request, 'edit_contract.html', {'form': form})




@login_required
def delete_contract(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    if request.method == 'POST':
        contract.delete()
        return redirect('contrat')
    return render(request, 'delete_contract.html', {'contract': contract})

def accueil(request):
    return render(request, 'accueil.html')

def welcome(request):
    return render(request, 'welcome.html')

@login_required
def dashboard(request):
    contracts = Contract.objects.filter(user=request.user)
    
    # Calcul des statistiques
    contract_types = contracts.values('contract_type').annotate(count=Count('contract_type'))
    contract_statuses = contracts.values('status').annotate(count=Count('status'))

    return render(request, 'dashboard.html', {
        'contract_types': list(contract_types),
        'contract_statuses': list(contract_statuses)
    })

@login_required
def add_contract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.user = request.user
            contract.save()
            return redirect('contrat')
    else:
        form = ContractForm()
    return render(request, 'add_contract.html', {'form': form})

def generate_pdf(request, contract_id):
    contract = Contract.objects.get(id=contract_id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="contract_{contract.contract_number}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)

    p.drawString(100, 750, f"Contract Number: {contract.contract_number}")
    p.drawString(100, 730, f"Client Name: {contract.client_name}")
    p.drawString(100, 710, f"Client Mail: {contract.client_mail}")
    p.drawString(100, 690, f"Expiration Date: {contract.expiration_date}")
    p.drawString(100, 670, f"Product: {contract.product}")
    p.drawString(100, 650, f"Contract Type: {contract.contract_type}")
    p.drawString(100, 630, f"Purchase Price: {contract.purchase_price}")
    p.drawString(100, 610, f"Selling Price: {contract.selling_price}")
    p.drawString(100, 590, f"Remaining Months: {contract.remaining_month}")
    p.drawString(100, 570, f"Status: {contract.get_status_display()}")

    p.showPage()
    p.save()
    
    return response

@login_required
def contract_history(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    history = ContractHistory.objects.filter(contract=contract).order_by('-change_date')
    return render(request, 'contract_history.html', {'contract': contract, 'history': history})


@staff_member_required
def all_modifications(request):
    history = ContractHistory.objects.select_related('user', 'contract').order_by('-change_date')
    return render(request, 'all_modifications.html', {'history': history}) 

@login_required
def calendar(request):
    return render(request, 'calendar.html')

@login_required
def calendar_data(request):
    contracts = Contract.objects.filter(user=request.user)
    events = []
    for contract in contracts:
        events.append({
            'title': f'Expiration: {contract.contract_number}',
            'start': contract.expiration_date.isoformat(),
            'color': 'red' if contract.status == 'near_expiry' else 'blue',
            'description': f"Contrat: {contract.contract_number}<br>Client: {contract.client_name}<br>Status: {contract.get_status_display()}<br>Type: {contract.contract_type}",
        })
        if contract.birthday_date:
            events.append({
                'title': f'Anniversaire: {contract.contract_number}',
                'start': contract.birthday_date.isoformat(),
                'color': 'green',
                'description': f"Contrat: {contract.contract_number}<br>Client: {contract.client_name}<br>Status: {contract.get_status_display()}<br>Type: {contract.contract_type}",
            })
    return JsonResponse(events, safe=False)
