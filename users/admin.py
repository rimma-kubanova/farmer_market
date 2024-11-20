from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, BuyerProfile, FarmerProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'delivery_address')
    search_fields = ('user__username',)

@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_id')
    search_fields = ('user__username',)
