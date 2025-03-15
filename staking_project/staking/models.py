from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet_address = models.CharField(max_length=255, blank=True, null=True)  # Adresse du wallet

    def __str__(self):
        return f"{self.user.username} - {self.wallet_address}"
