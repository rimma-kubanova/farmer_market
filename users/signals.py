from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, BuyerProfile, FarmerProfile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'buyer':
            BuyerProfile.objects.create(user=instance)
        elif instance.role == 'farmer':
            FarmerProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if instance.role == 'buyer' and hasattr(instance, 'buyer_profile'):
        instance.buyer_profile.save()
    elif instance.role == 'farmer' and hasattr(instance, 'farmer_profile'):
        instance.farmer_profile.save()
