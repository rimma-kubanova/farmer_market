from django.db import models
from django.conf import settings

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('fruits', 'Fruits'),
        ('vegetables', 'Vegetables'),
        ('mushroom', 'Mushroom'),
        ('dairy', 'Dairy'),
        ('oats', 'Oats'),
        ('bread', 'Bread'),
    ]

    PRODUCT_NAME_CHOICES = {
        'fruits': ['Banana', 'Apple', 'Orange', 'Grape', 'Mango'],
        'vegetables': ['Carrot', 'Potato', 'Onion', 'Cucumber', 'Pepper'],
        'mushroom': ['Button Mushroom', 'Portobello', 'Shiitake', 'Chanterelle', 'Enoki'],
        'dairy': ['Milk', 'Cheese', 'Butter', 'Yogurt', 'Cream'],
        'oats': ['Oatmeal', 'Granola', 'Muesli', 'Oat Bran', 'Steel-Cut Oats'],
        'bread': ['Sourdough', 'Baguette', 'Ciabatta', 'Rye Bread', 'Whole Wheat Bread'],
    }

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='fruits')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.category})"


class FarmerProduct(models.Model):
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='farmer_products'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='farmer_products'
    )
    available_quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('farmer', 'product')

    def __str__(self):
        return f"{self.farmer.username} - {self.product.name}"

from django.db import models
from django.conf import settings

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    farmer_product = models.ForeignKey(FarmerProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.price

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    farmer_product = models.ForeignKey('FarmerProduct', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.farmer_product.product.name} in {self.cart.user.username}'s cart"
