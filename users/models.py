from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('farmer', 'Farmer'),
        ('superuser', 'Superuser'),
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)

class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile')
    delivery_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Buyer Profile: {self.user.username}"

class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    farm_size = models.PositiveIntegerField(default=0)
    farm_location = models.CharField(max_length=255, blank=True, null=True)
    document_id = models.CharField(max_length=255, blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Farmer Profile: {self.user.username}"
    
