from django import forms
from .models import Contract

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = [
            'contract_number', 'client_name', 'client_mail', 'expiration_date', 'birthday_date', 
            'product', 'contract_type', 'purchase_price', 'selling_price', 'remaining_month', 'status', 'document'
        ]

    product = forms.ChoiceField(choices=Contract.PRODUCT_CHOICES, required=True)

