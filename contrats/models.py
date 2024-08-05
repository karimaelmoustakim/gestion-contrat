from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from notifications.models import Notification
from datetime import timedelta

class Contract(models.Model):
    STATUS_CHOICES = [
        ('active', 'active'),
        ('expired', 'expired'),
        ('near_expiry', 'near_expiry')
    ]
    
    PRODUCT_CHOICES = [
        ('revit', 'Revit'),
        ('archicad', 'Archicad'),
        ('sketchup', 'Sketchup Pro'),
        ('enscape', 'Enscape'),
        ('twinmotion', 'Twinmotion'),
        ('lumion', 'Lumion'),
        ('autocad', 'Autocad Architecture'),
        ('3dsmax', '3Ds Max')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contract_number = models.CharField(max_length=100)
    client_name = models.CharField(max_length=100)
    client_mail = models.EmailField()
    expiration_date = models.DateField()
    product = models.CharField(max_length=100, choices=PRODUCT_CHOICES)
    contract_type = models.CharField(max_length=100, null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    remaining_month = models.IntegerField(null=True, blank=True)
    birthday_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='active')
    document = models.FileField(upload_to='documents/', null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.contract_number

    def save(self, *args, **kwargs):
        self.update_status()
        super().save(*args, **kwargs)
        if self.status == 'near_expiry':
            notification, created = Notification.objects.get_or_create(
                user=self.user,
                contract=self,
                defaults={'message': f"Le contrat {self.contract_number} pour {self.client_name} expire bientôt."}
            )
            if not created:
                notification.message = f"Le contrat {self.contract_number} pour {self.client_name} expire bientôt."
                notification.save()
        else:
            Notification.objects.filter(contract=self).delete()

    def update_status(self):
        if self.expiration_date:
            days_remaining = (self.expiration_date - timezone.now().date()).days
            if days_remaining <= 0:
                self.status = 'expired'
            elif days_remaining <= 60:
                self.status = 'near_expiry'
            else:
                self.status = 'active'

class ContractHistory(models.Model):
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    change_description = models.TextField()
    change_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for {self.contract.contract_number} by {self.user.username}"
