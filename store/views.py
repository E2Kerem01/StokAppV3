import logging
import string

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from .forms import QuickAddForm, ProductForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Product, QuickAdd

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

@login_required(login_url='sistem')
def quickadd(request):
    if request.method == 'POST':
        form = QuickAddForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user  # Oluşturan kullanıcıyı atama
            product.save()
            return redirect('dashboard')  # Dashboard'a geri dön
    else:
        form = QuickAddForm()

    context = {'form': form}
    return render(request, 'quickadd.html', context)


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
