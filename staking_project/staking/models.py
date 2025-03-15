from django.db import models

class UserTransaction(models.Model):
    user_address = models.CharField(max_length=42)  # L'adresse Ethereum de l'utilisateur
    action = models.CharField(max_length=10)  # Action: 'stake', 'unstake', etc.
    amount = models.DecimalField(max_digits=18, decimal_places=8)  # Montant en FT42
    transaction_hash = models.CharField(max_length=66)  # Hash de la transaction
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.amount} FT42"
