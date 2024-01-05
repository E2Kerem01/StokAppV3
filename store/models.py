from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
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


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.CharField(max_length=255, default='')
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class QuickAdd(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=120, unique=True, null=False)
    stock = models.PositiveIntegerField(null=False)
    maaliyet = models.PositiveIntegerField(null=False)
    satisFiyati = models.PositiveIntegerField(null=False)
    kdvOrani = models.PositiveIntegerField(default=0)
    barkodNo = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    currency_choices = [
        ('TRY', 'TRY'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    ]
    currency = models.CharField(max_length=3, null=False, choices=currency_choices, default='USD')
    created_day = models.DateTimeField(default=timezone.now)  # Burada created_day ekleniyor.

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=120, unique=True)
    sortno = models.PositiveIntegerField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


# MEHMET KOD
class SalesPerson(models.Model):
    name = models.CharField(max_length=100, verbose_name='İsim', unique=True)
    phone_number = models.CharField(max_length=15, verbose_name='Telefon Numarası', unique=True)
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Borç')
    item_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Mal Fiyatı')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Satış Yapan Kişiler'


class Sales(models.Model):
    product = models.ForeignKey('QuickAdd', on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    sold_to = models.ForeignKey(User, on_delete=models.CASCADE)
    sold_by = models.ForeignKey(SalesPerson, on_delete=models.CASCADE, related_name='sales_by_person', null=True, blank=True)
    date_sold = models.DateTimeField(default=timezone.now)
    is_credit = models.BooleanField(default=False)

    def total_profit_margin(self):
        return (self.product.satisFiyati - self.product.maaliyet) * self.quantity_sold




# silme yeriii

@receiver(post_save, sender=QuickAdd)
def delete_quickadd(sender, instance, **kwargs):
    if instance.stock == 0:
        try:
            with transaction.atomic():
                instance.delete()
        except QuickAdd.DoesNotExist:
            pass
        except Exception as e:
            print(f'Hata oluştu: {e}')