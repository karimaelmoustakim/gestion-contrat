from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contract = models.ForeignKey('contrats.Contract', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'contract')  # Ajoute une contrainte d'unicité

    def __str__(self):
        return f"Notification for {self.contract.contract_number}"
