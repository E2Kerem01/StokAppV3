from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone



# Create your models here.
class Store(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="yazar")
    title = models.CharField(max_length=50, verbose_name="başlık")
    content = models.TextField(verbose_name="içerik")
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


"""class QuickProduct(models.Model):
    name = models.CharField(max_length=100)
    stock_quantity = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    category = models.CharField(max_length=50)  # veya ayrı bir Category modeli olabilir
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2) """


class Categories(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class QuickAdd(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=120, unique=True)
    stock = models.PositiveIntegerField()
    maaliyet = models.PositiveIntegerField()
    satisFiyati = models.PositiveIntegerField()
    kdvOrani = models.PositiveIntegerField()
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True)
    currency_choices = [
        ('TRY', 'TRY'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    ]
    currency = models.CharField(max_length=3, choices=currency_choices, default='USD')
    created_day = models.DateTimeField(default=timezone.now)  # Burada created_day ekleniyor.

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=120, unique=True)
    sortno = models.PositiveIntegerField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Sales(models.Model):
    product = models.ForeignKey('QuickAdd', on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    sold_to = models.ForeignKey(User, on_delete=models.CASCADE)
    date_sold = models.DateTimeField(auto_now_add=True)

    def total_profit_margin(self):
        return (self.product.satisFiyati - self.product.maaliyet) * self.quantity_sold