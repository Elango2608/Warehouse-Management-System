from django.db import models # type: ignore
from suppliers.models import Supplier
from django.core.validators import MinValueValidator # type: ignore

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=50, unique=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products'
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name='products'
    )

    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock_quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class StockIn(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='stock_in_records'
    )

    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    reference_number = models.CharField(
        max_length=100,
        unique=True
    )

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Stock In - {self.product.name} ({self.quantity})"


class StockOut(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='stock_out_records'
    )

    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    reference_number = models.CharField(
        max_length=100,
        unique=True
    )

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Stock Out - {self.product.name} ({self.quantity})"