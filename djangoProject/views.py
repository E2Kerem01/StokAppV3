from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.shortcuts import render

from store.forms import QuickAddForm
from store.models import QuickAdd


# @login_required(login_url='sistem')
# def dashboard(request):
#     form = QuickAddForm()
#     user_products = QuickAdd.objects.filter(user=request.user)

#     product_count = user_products.count()
#
#     return render(request, 'dashboard.html', {'form': form, 'product_count': product_count})


# @login_required(login_url='sistem')
# def dashboard(request):
#     form = QuickAddForm()  # Formu oluştur
#     user_products = QuickAdd.objects.filter(user=request.user)
#     product_count = user_products.count()
#     total_expense = sum(product.maaliyet * product.stock for product in user_products)
#
#     if request.method == 'POST':
#         form = QuickAddForm(request.POST)
#         if form.is_valid():
#             form.save()  # Formu kaydet
#             # Ekleme işlemi başarılı olduğunda product_count'u güncelle
#             user_products = QuickAdd.objects.filter(user=request.user)
#             product_count = user_products.count()
#             total_expense = sum(product.maaliyet * product.stock for product in user_products)
#
#     return render(request, 'dashboard.html', {'form': form, 'product_count': product_count, 'total_expense': total_expense})


@login_required(login_url='sistem')
def dashboard(request):
    form = QuickAddForm()
    user_products = QuickAdd.objects.filter(user=request.user)
    product_count = user_products.count()
    total_cost = user_products.annotate(total=Sum(F('maaliyet') * F('stock'))) \
                     .aggregate(total_cost=Sum('total'))['total_cost'] or 0

    if request.method == 'POST':
        form = QuickAddForm(request.POST)
        if form.is_valid():
            form.save()
            user_products = QuickAdd.objects.filter(user=request.user)
            product_count = user_products.count()
            total_cost = user_products.annotate(total=Sum(F('maaliyet') * F('stock'))) \
                             .aggregate(total_cost=Sum('total'))['total_cost'] or 0
    return render(request, 'dashboard.html',
                  {'form': form, 'product_count': product_count, 'total_cost': total_cost})
