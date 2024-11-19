from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('farmer', 'Farmer'),
        ('superuser', 'Superuser'),
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)

# class BuyerProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='buyer_profile')
#     # preferred_categories = models.TextField()

# class FarmerProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='farmer_profile')
#     # farm_size = models.DecimalField(max_digits=10, decimal_places=2)
