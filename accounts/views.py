from django.shortcuts import render # type: ignore
from django.shortcuts import render, redirect # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth import login  # type: ignore
from .forms import RegisterForm
from django.contrib.auth import authenticate, login # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib.auth import logout # type: ignore
from django.db.models import Sum, F # type: ignore

from inventory.models import Product, Category, StockIn, StockOut
from suppliers.models import Supplier

# Create your views here.

def home_view(request):
    return render(request, 'accounts/home.html')

def register_view(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            messages.success(
                request,
                'Registration successful! Welcome to WMS.'
            )

            return redirect('dashboard')

    else:
        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                'Login successful!'
            )

            return redirect('dashboard')

        else:
            messages.error(
                request,
                'Invalid username or password.'
            )

    return render(request, 'accounts/login.html')


@login_required
def dashboard_view(request):

    # 1. Total number of products
    total_products = Product.objects.count()

    # 2. Total number of suppliers
    total_suppliers = Supplier.objects.count()

    # 3. Total number of categories
    total_categories = Category.objects.count()

    # 4. Total stock units
    total_stock_units = Product.objects.aggregate(
        total=Sum('stock_quantity')
    )['total'] or 0

    # 5. Low stock products
    low_stock_products = Product.objects.filter(
        stock_quantity__lte=F('reorder_level')
    ).count()

    # 6. Retrieve recent Stock In transactions
    stock_in_records = StockIn.objects.select_related(
        'product'
    ).order_by('-created_at')[:5]

    # 7. Retrieve recent Stock Out transactions
    stock_out_records = StockOut.objects.select_related(
        'product'
    ).order_by('-created_at')[:5]

    recent_transactions = []

    for record in stock_in_records:
        record.transaction_type = 'Stock In'
        record.display_quantity = f'+{record.quantity}'
        recent_transactions.append(record)

    for record in stock_out_records:
        record.transaction_type = 'Stock Out'
        record.display_quantity = f'-{record.quantity}'
        recent_transactions.append(record)

    # Sort transactions by latest date
    recent_transactions.sort(
        key=lambda record: record.created_at,
        reverse=True
    )

    recent_transactions = recent_transactions[:5]

    context = {
        'total_products': total_products,
        'total_suppliers': total_suppliers,
        'total_categories': total_categories,
        'total_stock_units': total_stock_units,
        'low_stock_products': low_stock_products,
        'recent_transactions': recent_transactions,
    }

    return render(
        request,
        'accounts/dashboard.html',
        context
    )

def logout_view(request):

    logout(request)

    messages.success(request, 'You have been logged out.')

    return redirect('login')

