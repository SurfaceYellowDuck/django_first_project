from django.db import models

# Create your models here.
from geekshop import settings
from mainapp.models import Product, ProductCategory


from django.db import models


def total_price():
    total_price = 0
    for el in Product.objects.all():
        total_price += el.price * el.quantity
    return total_price


def total_quantity():
    total_quantity = 0
    for el in Basket.objects.all():
        total_quantity += el.quantity
    return total_quantity


class Basket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='basket',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0,
    )
    add_datetime = models.DateTimeField(
        verbose_name='время',
        auto_now_add=True,
    )
