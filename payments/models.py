from django.db import models
from django.contrib.auth.models import User
from contrats.models import Contract

class Payment(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_payments')
    created_at = models.DateTimeField(auto_now_add=True)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Nouveau champ


    def __str__(self):
        return f"Payment for {self.contract.contract_number} - {self.amount}"
