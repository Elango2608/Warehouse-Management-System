from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib import messages # type: ignore
from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.db.models.deletion import ProtectedError # type: ignore

# Create your views here.

from .models import Supplier
from .forms import SupplierForm


@login_required
def supplier_list(request):

    suppliers = Supplier.objects.all().order_by('-created_at')

    return render(
        request,
        'suppliers/supplier_list.html',
        {'suppliers': suppliers}
    )


@login_required
def supplier_create(request):

    if request.method == 'POST':

        form = SupplierForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Supplier added successfully!'
            )

            return redirect('supplier_list')

    else:
        form = SupplierForm()

    return render(
        request,
        'suppliers/supplier_form.html',
        {'form': form}
    )

@login_required
def supplier_update(request, supplier_id):

    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Supplier updated successfully!'
            )

            return redirect('supplier_list')

    else:
        form = SupplierForm(instance=supplier)

    return render(
        request,
        'suppliers/supplier_form.html',
        {
            'form': form,
            'title': 'Update Supplier'
        }
    )


@login_required
def supplier_delete(request, supplier_id):

    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == 'POST':
        try:
            supplier.delete()
            messages.success(request, 'Supplier deleted successfully!')

        except ProtectedError:
            messages.error(
                request,
                'Cannot delete this supplier because products are linked to it.'
            )

        return redirect('supplier_list')

    return render(
        request,
        'suppliers/supplier_confirm_delete.html',
        {'supplier': supplier}
    )