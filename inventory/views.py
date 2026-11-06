from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.core.exceptions import ValidationError # type: ignore
from django.db.models import Q # type: ignore
from django.db.models.deletion import ProtectedError # type: ignore

from .models import Category, Product, StockIn, StockOut
from .forms import CategoryForm, ProductForm, StockInForm, StockOutForm
from .services import add_stock, remove_stock


# ==========================================
# CATEGORY MANAGEMENT
# ==========================================

@login_required
def category_list(request):

    categories = Category.objects.all().order_by('name')

    context = {
        'categories': categories
    }

    return render(
        request,
        'inventory/category_list.html',
        context
    )


@login_required
def category_create(request):

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('category_list')

    else:
        form = CategoryForm()

    context = {
        'form': form,
        'title': 'Add Category'
    }

    return render(
        request,
        'inventory/category_form.html',
        context
    )


@login_required
def category_update(request, category_id):

    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')

    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'title': 'Update Category',
        'category': category
    }

    return render(
        request,
        'inventory/category_form.html',
        context
    )


@login_required
def category_delete(request, category_id):

    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        try:
            category.delete()
            messages.success(request, 'Category deleted successfully!')

        except ProtectedError:
            messages.error(
                request,
                'Cannot delete this category because products are linked to it.'
            )

        return redirect('category_list')

    context = {
        'category': category
    }

    return render(
        request,
        'inventory/category_confirm_delete.html',
        context
    )


# ==========================================
# PRODUCT MANAGEMENT
# ==========================================

@login_required
def product_list(request):

    products = Product.objects.select_related(
        'category',
        'supplier'
    ).all().order_by('name')

    # Search by product name or SKU
    search_query = request.GET.get('search', '').strip()

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(sku__icontains=search_query)
        )

    # Filter by category
    category_id = request.GET.get('category', '')

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all().order_by('name')

    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id
    }

    return render(
        request,
        'inventory/product_list.html',
        context
    )


@login_required
def product_create(request):

    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_list')

    else:
        form = ProductForm()

    context = {
        'form': form,
        'title': 'Add Product'
    }

    return render(
        request,
        'inventory/product_form.html',
        context
    )


@login_required
def product_update(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')

    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'title': 'Update Product',
        'product': product
    }

    return render(
        request,
        'inventory/product_form.html',
        context
    )


@login_required
def product_delete(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        try:
            product.delete()
            messages.success(request, 'Product deleted successfully!')

        except ProtectedError:
            messages.error(
                request,
                'Cannot delete this product because stock transactions are linked to it.'
            )

        return redirect('product_list')

    context = {
        'product': product
    }

    return render(
        request,
        'inventory/product_confirm_delete.html',
        context
    )


# ==========================================
# STOCK IN MANAGEMENT
# ==========================================

@login_required
def stock_in(request):

    if request.method == 'POST':
        form = StockInForm(request.POST)

        if form.is_valid():
            try:
                add_stock(
                    product_id=form.cleaned_data['product'].id,
                    quantity=form.cleaned_data['quantity'],
                    reference_number=form.cleaned_data['reference_number'],
                    notes=form.cleaned_data['notes']
                )

                messages.success(
                    request,
                    'Stock added successfully!'
                )

                return redirect('product_list')

            except ValidationError as error:
                messages.error(request, str(error))

        else:
            messages.error(
                request,
                'Please correct the form errors.'
            )

    else:
        form = StockInForm()

    return render(
        request,
        'inventory/stock_in.html',
        {'form': form}
    )


# ==========================================
# STOCK OUT MANAGEMENT
# ==========================================

@login_required
def stock_out(request):

    if request.method == 'POST':
        form = StockOutForm(request.POST)

        if form.is_valid():
            try:
                remove_stock(
                    product_id=form.cleaned_data['product'].id,
                    quantity=form.cleaned_data['quantity'],
                    reference_number=form.cleaned_data['reference_number'],
                    notes=form.cleaned_data['notes']
                )

                messages.success(
                    request,
                    'Stock removed successfully!'
                )

                return redirect('product_list')

            except ValidationError as error:
                messages.error(request, str(error))

        else:
            messages.error(
                request,
                'Please correct the form errors.'
            )

    else:
        form = StockOutForm()

    return render(
        request,
        'inventory/stock_out.html',
        {'form': form}
    )


# ==========================================
# TRANSACTION HISTORY
# SEARCH, FILTER AND DATE VALIDATION
# ==========================================

@login_required
def transaction_history(request):

    # 1. Get filter values from URL
    search_query = request.GET.get('search', '').strip()
    transaction_type = request.GET.get('type', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    date_error = ''

    # 2. Validate dates
    start = None
    end = None

    try:

        if start_date:
            start = datetime.strptime(
                start_date, '%Y-%m-%d'
            ).date()

        if end_date:
            end = datetime.strptime(
                end_date, '%Y-%m-%d'
            ).date()

        if start and end and start > end:
            date_error = 'Start date cannot be later than end date.'

    except ValueError:
        date_error = 'Please enter valid dates.'

    # 3. Retrieve Stock In records
    stock_in_records = StockIn.objects.select_related(
        'product'
    ).all()

    # 4. Retrieve Stock Out records
    stock_out_records = StockOut.objects.select_related(
        'product'
    ).all()

    # 5. Search by product name or SKU
    if search_query:

        search_filter = (
            Q(product__name__icontains=search_query) |
            Q(product__sku__icontains=search_query)
        )

        stock_in_records = stock_in_records.filter(search_filter)

        stock_out_records = stock_out_records.filter(search_filter)

    # 6. Filter by transaction type
    if transaction_type == 'stock_in':

        stock_out_records = stock_out_records.none()

    elif transaction_type == 'stock_out':

        stock_in_records = stock_in_records.none()

    # 7. Apply date filters only when dates are valid
    if date_error:

        stock_in_records = stock_in_records.none()
        stock_out_records = stock_out_records.none()

    else:

        if start:

            stock_in_records = stock_in_records.filter(
                created_at__date__gte=start
            )

            stock_out_records = stock_out_records.filter(
                created_at__date__gte=start
            )

        if end:

            stock_in_records = stock_in_records.filter(
                created_at__date__lte=end
            )

            stock_out_records = stock_out_records.filter(
                created_at__date__lte=end
            )

    # 8. Combine both transaction types
    transactions = []

    # Process Stock In records
    for record in stock_in_records:

        record.transaction_type = 'Stock In'
        record.display_quantity = f'+{record.quantity}'

        transactions.append(record)

    # Process Stock Out records
    for record in stock_out_records:

        record.transaction_type = 'Stock Out'
        record.display_quantity = f'-{record.quantity}'

        transactions.append(record)

    # 9. Sort newest transactions first
    transactions.sort(
        key=lambda record: record.created_at,
        reverse=True
    )

    # 10. Send data to HTML template
    context = {
        'transactions': transactions,
        'search_query': search_query,
        'transaction_type': transaction_type,
        'start_date': start_date,
        'end_date': end_date,
        'date_error': date_error,
    }

    return render(
        request,
        'inventory/transaction_history.html',
        context
    )