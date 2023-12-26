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


# @login_required(login_url='sistem')
# def dashboard(request):
#     form = QuickAddForm()
#     user_products = QuickAdd.objects.filter(user=request.user)
#     product_count = user_products.count()
#     total_cost = user_products.annotate(total=Sum(F('maaliyet') * F('stock'))) \
#                      .aggregate(total_cost=Sum('total'))['total_cost'] or 0
#
#     total_price = user_products.annotate(total1=Sum(F('satisFiyati') * F('stock'))) \
#                      .aggregate(total_price=Sum('total1'))['total_price'] or 0
#
#     if request.method == 'POST':
#         form = QuickAddForm(request.POST)
#         if form.is_valid():
#             form.save()
#             user_products = QuickAdd.objects.filter(user=request.user)
#             product_count = user_products.count()
#             total_cost = user_products.annotate(total=Sum(F('maaliyet') * F('stock'))) \
#                              .aggregate(total_cost=Sum('total'))['total_cost'] or 0
#
#             total_price = user_products.annotate(total=Sum(F('satisFiyati') * F('stock'))) \
#                               .aggregate(total_cost=Sum('total'))['total_price'] or 0
#
#     return render(request, 'dashboard.html',
#                   {'form': form, 'product_count': product_count, 'total_cost': total_cost, 'total_price': total_price})


@login_required(login_url='sistem')
def dashboard(request):
    form = QuickAddForm()
    user_products = QuickAdd.objects.filter(user=request.user)
    product_count = user_products.count()
    total_cost = user_products.annotate(total=Sum(F('maaliyet') * F('stock'))) \
                     .aggregate(total_cost=Sum('total'))['total_cost'] or 0

    total_price = user_products.annotate(totalv1=Sum(F('satisFiyati') * F('stock'))) \
                      .aggregate(total_price=Sum('totalv1'))['total_price'] or 0

    if request.method == 'POST':
        form = QuickAddForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['name']
            existing_product = QuickAdd.objects.filter(user=request.user, name=product_name).first()

            if existing_product:  # Eğer ürün zaten varsa, güncelle
                form = QuickAddForm(request.POST, instance=existing_product)
            else:  # Yoksa, yeni ürün oluştur
                form = QuickAddForm(request.POST)

            product = form.save(commit=False)
            product.user = request.user
            product.save()

            user_products = QuickAdd.objects.filter(user=request.user)
            product_count = user_products.count()
            total_cost = user_products.annotate(total=Sum(F('maaliyet') * F('stock'))) \
                             .aggregate(total_cost=Sum('total'))['total_cost'] or 0

            total_price = user_products.annotate(totalv1=Sum(F('satisFiyati') * F('stock'))) \
                              .aggregate(total_price=Sum('totalv1'))['total_price'] or 0

    return render(request, 'dashboard.html',
                  {'form': form, 'product_count': product_count, 'total_cost': total_cost, 'total_price': total_price})
