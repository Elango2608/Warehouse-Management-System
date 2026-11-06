from django.db import transaction # type: ignore
from django.core.exceptions import ValidationError # type: ignore

from .models import Product, StockIn, StockOut


@transaction.atomic
def add_stock(product_id, quantity, reference_number, notes=''):
    if quantity <= 0:
        raise ValidationError("Quantity must be greater than zero.")

    product = Product.objects.select_for_update().get(id=product_id)

    stock_record = StockIn.objects.create(
        product=product,
        quantity=quantity,
        reference_number=reference_number,
        notes=notes
    )

    product.stock_quantity += quantity
    product.save(update_fields=['stock_quantity', 'updated_at'])

    return stock_record


@transaction.atomic
def remove_stock(product_id, quantity, reference_number, notes=''):
    if quantity <= 0:
        raise ValidationError("Quantity must be greater than zero.")

    product = Product.objects.select_for_update().get(id=product_id)

    if product.stock_quantity < quantity:
        raise ValidationError("Insufficient stock available.")

    stock_record = StockOut.objects.create(
        product=product,
        quantity=quantity,
        reference_number=reference_number,
        notes=notes
    )

    product.stock_quantity -= quantity
    product.save(update_fields=['stock_quantity', 'updated_at'])

    return stock_record