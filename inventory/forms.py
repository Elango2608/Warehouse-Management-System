from django import forms # type: ignore
from .models import Category, Product
from .models import Category, Product, StockIn, StockOut


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category

        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter category description'
            }),
        }

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            'name',
            'sku',
            'category',
            'supplier',
            'description',
            'price',
            'reorder_level'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),

            'sku': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter unique SKU'
            }),

            'category': forms.Select(attrs={
                'class': 'form-select'
            }),

            'supplier': forms.Select(attrs={
                'class': 'form-select'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter product description'
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product price',
                'min': '0.01',
                'step': '0.01'
            }),

            'reorder_level': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
        }

from django import forms # type: ignore

from .models import Category, Product, StockIn, StockOut


# --------------------------------------------------
# CATEGORY FORM
# --------------------------------------------------

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter category description'
            }),
        }


# --------------------------------------------------
# PRODUCT FORM
# --------------------------------------------------

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'sku',
            'category',
            'supplier',
            'description',
            'price',
            'reorder_level'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'sku': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product SKU'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'supplier': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter product description'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'reorder_level': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
        }


# --------------------------------------------------
# STOCK IN FORM
# --------------------------------------------------

class StockInForm(forms.ModelForm):
    class Meta:
        model = StockIn
        fields = [
            'product',
            'quantity',
            'reference_number',
            'notes'
        ]

        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-select'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Enter quantity'
            }),
            'reference_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter unique reference number'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter additional notes (optional)'
            }),
        }

    def clean_reference_number(self):
        reference_number = self.cleaned_data['reference_number']

        stock_in_exists = StockIn.objects.filter(
            reference_number=reference_number
        ).exclude(pk=self.instance.pk).exists()

        stock_out_exists = StockOut.objects.filter(
            reference_number=reference_number
        ).exists()

        if stock_in_exists or stock_out_exists:
            raise forms.ValidationError(
                "This reference number has already been used."
            )

        return reference_number


# --------------------------------------------------
# STOCK OUT FORM
# --------------------------------------------------

class StockOutForm(forms.ModelForm):
    class Meta:
        model = StockOut
        fields = [
            'product',
            'quantity',
            'reference_number',
            'notes'
        ]

        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-select'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Enter quantity'
            }),
            'reference_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter unique reference number'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter additional notes (optional)'
            }),
        }

    def clean_reference_number(self):
        reference_number = self.cleaned_data['reference_number']

        stock_out_exists = StockOut.objects.filter(
            reference_number=reference_number
        ).exclude(pk=self.instance.pk).exists()

        stock_in_exists = StockIn.objects.filter(
            reference_number=reference_number
        ).exists()

        if stock_out_exists or stock_in_exists:
            raise forms.ValidationError(
                "This reference number has already been used."
            )

        return reference_number