import logging
import string

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView
from .forms import ProductForm, CategoryForm, SalesPersonForm
from .models import QuickAdd, SalesPerson, Sales

# Create your views here.


"""def addProduct(request):
    if request.method == "POST":
        form = QuickProductForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("")

    else:
        form = QuickProductForm()
    return render(request, 'index.html', {'form': form})"""


# @login_required(login_url='login')
# def quickadd(request):
#     if request.method == 'POST':
#         form = QuickAddForm(request.POST)
#         if form.is_valid():
#             product = form.save(commit=False)
#             product.user = request.user  # Oluşturan kullanıcıyı atama
#             product.save()
#             return render(request, 'dashboard.html', {'form': QuickAddForm()})
#     else:
#         form = QuickAddForm()
#
#     context = {'form': form}
#     return render(request, 'dashboard.html', context)

# @login_required(login_url='sistem')
# def quickadd(request):
#     if request.method == 'POST':
#         form = QuickAddForm(request.POST)
#         if form.is_valid():
#             product = form.save(commit=False)
#             product.user = request.user  # Oluşturan kullanıcıyı atama
#             product.save()
#             return redirect('dashboard')  # Dashboard'a geri dön
#     else:
#         form = QuickAddForm()
#
#     context = {'form': form}
#     return render(request, 'dashboard.html', context)


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        try:
            form.save()
        except Exception as e:
            print(f"Hata: {e}")
        return redirect('dashboard')
    else:
        form = ProductForm()

    context = {'form': form}
    return render(request, 'store/create_product.html', context)


@login_required(login_url='sistem')
def productmanagement(request):
    # Kullanıcıya ait ürünleri sıralamak için
    user_products = QuickAdd.objects.filter(user=request.user).order_by('-created_day')

    # Eğer bir arama yapılıyorsa
    query = request.GET.get('q')
    if query:
        user_products = user_products.filter(name__icontains=query)

    # Eğer bir ürün eklemesi yapılıyorsa
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('product_list')  # Ürün eklendikten sonra tekrar listeye yönlendir
    else:
        form = ProductForm()

    return render(request, 'store/productmanagement.html', {'products': user_products, 'form': form})


@login_required(login_url='sistem')
def category(request):
    forms = CategoryForm()
    if request.method == 'POST':
        forms = CategoryForm(request.POST)
        if forms.is_valid():
            category = forms.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('category')
    context = {
        'form': forms
    }
    return render(request, 'store/category.html', context)


# MEHMET KOD

class SalesPersonDeleteView(DeleteView):
    model = SalesPerson
    template_name = 'store/salesperson_confirm_delete.html'
    success_url = reverse_lazy('salesperson_list')


class SalesPersonUpdateView(UpdateView):
    model = SalesPerson
    form_class = SalesPersonForm
    template_name = 'store/salesperson_form.html'
    success_url = reverse_lazy('salesperson_list')


def salesperson_list(request):
    salespeople = SalesPerson.objects.all()
    return render(request, 'store/salesperson_list.html', {'salespeople': salespeople})


def create_salesperson(request):
    if request.method == 'POST':
        form = SalesPersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salesperson_list')
    else:
        form = SalesPersonForm()

    return render(request, 'store/salesperson_form.html', {'form': form})


def salesperson_detail(request, pk):
    salesperson = get_object_or_404(SalesPerson, pk=pk)
    return render(request, 'store/salesperson_detail.html', {'salesperson': salesperson})


# @login_required(login_url='login')
# def product_sales_history(request, product_id):
#     product = get_object_or_404(QuickAdd, id=product_id)
#     sales_history = Sales.objects.filter(product=product)
#
#     # Ürünün toplam karını hesapla
#     total_quantity_sold = Sales.objects.filter(product=product).aggregate(Sum('quantity_sold'))['quantity_sold__sum']
#     total_profit1 = total_quantity_sold * (product.satisFiyati - product.maaliyet)
#     return render(request, 'store/sales_history.html',
#                   {'product': product, 'sales_history': sales_history, 'total_profit1': total_profit1}, )

@login_required(login_url='login')
def product_sales_history(request, product_id):
    product = get_object_or_404(QuickAdd, id=product_id)
    sales_history = Sales.objects.filter(product=product)
    user_sales = Sales.objects.filter(sold_by=request.user)

    # Ürünün toplam karını hesapla
    total_profit = 0

    for sale in user_sales:
        product_quantity = sale.quantity_sold
        product_price = sale.product.satisFiyati  # Ürünün satış fiyatı, bu kısım modele göre uyarlanmalı

        # Her bir satışın karını hesaplayıp toplam kara ekleyelim
        total_profit += product_quantity * product_price

    return render(request, 'store/sales_history.html',
                  {'product': product, 'sales_history': sales_history, 'total_profit': total_profit})


@login_required(login_url='login')
def sales_history(request):
    sales = Sales.objects.filter(sold_to=request.user)
    return render(request, 'store/sales_history.html', {'sales': sales})


def calculate_profit_margin(product):
    return product.satisFiyati - product.maaliyet


def update_total_profit_margin(total_profit_margin, profit_margin):
    return total_profit_margin + profit_margin


@login_required(login_url='login')
def quick_sale_page(request):
    total_profit_margin = 0
    search_term = request.GET.get('search', '')

    if request.user.is_authenticated:
        if search_term:
            # Eğer search_term değeri boş değilse, ürünleri filtrele
            products = QuickAdd.objects.filter(user=request.user, name__icontains=search_term)
        else:
            products = QuickAdd.objects.none()

        product_count = products.count()

        if request.method == 'POST':

            product_id = request.POST.get('product_id')
            quantity_sold = int(request.POST.get('quantity_sold'))

            product = QuickAdd.objects.get(id=product_id)

            if product.stock >= quantity_sold:

                product.stock -= quantity_sold
                product.save()

                # Kar marjını güncelle
                profit_margin = calculate_profit_margin(product) * quantity_sold
                total_profit_margin = update_total_profit_margin(total_profit_margin, profit_margin)

                sales = Sales.objects.create(
                    product=product,
                    quantity_sold=quantity_sold,
                    sold_to=request.user  # Satışı yapan kullanıcı
                )

            else:
                messages.error(request, 'yetersiz stok')

        # Satış geçmişini al
        sales_history = Sales.objects.filter(product__user=request.user)

        return render(request, 'store/sales.html', {
            'products': products,
            'product_count': product_count,
            'search_term': search_term,
            'total_profit_margin': total_profit_margin,
            'sales_history': sales_history
        })
    else:
        return redirect('login')


def quick_sale(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity_sold = request.POST.get('quantity_sold')

        product = get_object_or_404(QuickAdd, id=product_id)
        if product.stock >= int(quantity_sold):
            # ...

            messages.success(request, 'Ürün başarıyla satıldı.')

            # İlgili ürünün satış geçmişine yönlendir
            return redirect(reverse('product_sales_history', args=[product.id]))
        else:
            messages.error(request, 'Satış için yeterli stok yok.')

    return redirect('dashboard')
