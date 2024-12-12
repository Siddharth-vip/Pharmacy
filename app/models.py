from django.contrib.auth import get_user_model
from django.db import models
import uuid

User = get_user_model()

class CustomUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    profile_image = models.ImageField(upload_to='users')
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

    
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(upload_to='products')
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    description = models.TextField()
    benefits = models.TextField()
    how_to_use = models.TextField()
    precaution = models.TextField()
    weight = models.PositiveIntegerField()
    categories = models.CharField(max_length=200)

    def get_categories(self):
        return self.categories.split(',')
    
    def save(self, *args, **kwargs):    
        category_names = self.get_categories()
        for category_name in category_names:
            category_name = category_name.strip()
            if category_name:
                Category.objects.get_or_create(name=category_name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def cart_price(self):
       return sum(item.total_price for item in self.cartitem_set.all())

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_price(self):
        return self.quantity * self.product.price
    
    def add_item(self):
        self.quantity += 1
        self.save()

    def remove_item(self):
        if self.quantity > 1:
            self.quantity -= 1
            self.save()
            return True
        else:
            self.delete()
            return False

    def delete_product(self):
        self.delete()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
 
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories',null=True)

    def __str__(self):
        return self.name