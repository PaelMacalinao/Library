from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    product_list = models.ManyToManyField('Product', through='CartItem', related_name='carts')

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in {self.cart}"

class Product(models.Model):
    title = models.CharField(max_length=255, null=True)
    pageCount = models.PositiveIntegerField(default=0)
    description = models.TextField(null=True)
    thumbnailUrl = models.URLField(blank=True, null=True)
    authors = models.JSONField(null=True)
    categories = models.JSONField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)

    def __str__(self):
        return self.title

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(Product, through='OrderItem')
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in Order #{self.order.pk}"

class PurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    orders = models.ManyToManyField(Order)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)  
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PurchaseHistory for {self.user.username} on {self.purchase_date}"


@receiver(post_save, sender=User)
def create_or_update_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
    else:
        instance.cart.save()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()