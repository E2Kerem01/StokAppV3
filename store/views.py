import logging
import string

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import DeleteView, UpdateView
from .forms import ProductForm, CategoryForm, SalesPersonForm, QuickAddForm
from .models import QuickAdd, SalesPerson, Sales
import json

logger = logging.getLogger(__name__)


# Create your views here.


class QuickAddUpdate(UpdateView):
    model = QuickAdd
    form_class = QuickAddForm
    template_name = 'store/quickadd.html'
    success_url = reverse_lazy('productmanagement')


# def product_list(request):
#     product_lists = QuickAdd.objects.all()
#     paginator = Paginator(product_lists, 10)  # 10 ürünün olduğu bir sayfa
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'store/productmanagement.html', {'page_obj': page_obj})
#

@csrf_exempt
def update_product(request, pk):
    if request.method == 'POST':
        # JSON verisini al
        data = json.loads(request.body)

        # İlgili ürünü veritabanından al
        product = QuickAdd.objects.get(pk=pk)

        # JSON payload'ından gelen verilerle ilgili alanları güncelle
        product.name = data.get('name', product.name)
        product.stock = data.get('stock', product.stock)
        product.maaliyet = data.get('maaliyet', product.maaliyet)
        product.satisFiyati = data.get('satisfiyati', product.satisFiyati)
        product.currency = data.get('birim', product.currency)
        product.barkodNo = data.get('barkodNo', product.barkodNo)
        # Diğer alanlar için aynı işlemi yapın

        # Güncellenmiş ürünü kaydet
        product.save()

        return JsonResponse({'success': True})  # Başarılı yanıt
    else:
        return JsonResponse({'error': 'Geçersiz istek'})


# @csrf_exempt
# @login_required(login_url='sistem')
# def update_product(request, pk):
#     if request.method == 'POST':
#         updated_name = request.POST.get('name')
#         updated_stock = request.POST.get('stock')
#         updated_maaliyet = request.POST.get('maaliyet')
#         updated_satis_fiyati = request.POST.get('satisFiyati')
#         updated_birim = request.POST.get('birim')
#         updated_barkod_no = request.POST.get('barkodNo')
#
#         try:
#             product = QuickAdd.objects.get(pk=pk, user=request.user)
#             product.name = updated_name
#             product.stock = updated_stock
#             product.maaliyet = updated_maaliyet
#             product.satisFiyati = updated_satis_fiyati
#             product.birim = updated_birim
#             product.barkodNo = updated_barkod_no
#
#             product.save()
#             return JsonResponse({'success': True})  # Başarılı olduğunda JSON yanıtı
#         except QuickAdd.DoesNotExist:
#             return JsonResponse({'success': False, 'error': 'Ürün bulunamadı'})  # Hata durumunda JSON yanıtı
#
#     return JsonResponse({'success': False, 'error': 'Geçersiz istek'})  # Diğer durumlarda geçersiz istek yanıtı

# @csrf_exempt
# @login_required(login_url='sistem')
# def update_product(request, pk):
#     # Mevcut ürünü al
#     product = get_object_or_404(QuickAdd, pk=pk)
#
#     if request.method == 'POST':
#         print("asdf")
#         # Mevcut verilerle formu doldur
#         form = QuickAddForm(request.POST, instance=product)
#
#         if form.is_valid():
#             # Sadece belirli alanları güncelle
#             updated_name = form.cleaned_data['name']
#             updated_stock = form.cleaned_data['stock']
#             print(updated_stock)
#             updated_maaliyet = form.cleaned_data['maaliyet']
#             updated_satisFiyati = form.cleaned_data['satisFiyati']
#             updated_currency = form.cleaned_data['currency']
#             updated_barkodNo = form.cleaned_data['barkodNo']
#             # Diğer güncellenmesi gereken alanları da buraya ekleyin
#
#             # Yalnızca değiştirilen alanları güncelle
#             product.name = updated_name
#             print(product.name)
#             product.stock = updated_stock
#             product.maaliyet = updated_maaliyet
#             product.satisFiyati = updated_satisFiyati
#             product.currency = updated_currency
#             product.barkodNo = updated_barkodNo
#             # Diğer alanları da güncelleyin
#
#             product.save()  # Değiştirilen alanları kaydet
#
#             return JsonResponse({'success': True})  # Başarılı olduğunda JSON yanıtı
#         else:
#             # print(form.errors)
#             return JsonResponse({'success': False, 'error': 'Form geçersiz'})  # Hata durumunda JSON yanıtı
#
#     # GET istekleri için formu doldur
#     else:
#         form = QuickAddForm(instance=product)
#
#     # Formu ve diğer gereklilikleri döndür
#     context = {'form': form}
#     return render(request, 'store/productmanagement.html', context)


# @csrf_exempt
# @login_required(login_url='sistem')
# def update_product(request, pk):
#
#     if request.method == 'POST':
#         form = QuickAddForm(request.POST)
#         user_products = QuickAdd.objects.filter(user=request.user)
#         if form.is_valid():
#             product = form.save(commit=False)
#             product.user = request.user
#             product.save()
#             return JsonResponse({'success': True})  # Başarılı olduğunda JSON yanıtı
#
#         else:  # Eğer ürün yoksa yeni ürün oluştur
#             form = QuickAddForm(request.POST)


# @login_required(login_url='sistem')
# def update_product(request, pk):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         try:
#             product = QuickAdd.objects.get(pk=pk)
#
#             for field, value in data.items():
#                 setattr(product, field, value)
#
#             product.save()
#             return JsonResponse({'success': True})
#         except QuickAdd.DoesNotExist:
#             return JsonResponse({'success': False, 'error': 'Ürün bulunamadı'})
#     return JsonResponse({'success': False, 'error': 'Geçersiz istek'})
#
#
# @login_required(login_url='sistem')
# def delete_product(request, pk):
#     if request.method == 'POST':
#         product = QuickAdd.objects.get(pk=pk)
#         product.delete()
#         return JsonResponse({'success': True})
#     return JsonResponse({'success': False})


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
    query = request.GET.get('product_name')
    if query:
        user_products = user_products.filter(user=request.user, name__icontains=query)

    paginator = Paginator(user_products, 10)  # Her sayfada 10 ürün gösterilecek
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

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

    return render(request, 'store/productmanagement.html', {'products': user_products, 'form': form,
                                                            'page_obj': page_obj})


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


@csrf_exempt
@login_required(login_url='sistem')
def update_stock(request, pk):
    if request.method == 'POST' and request.is_ajax():
        try:
            product = QuickAdd.objects.get(pk=pk, user=request.user)
            field = request.POST.get('field')
            value = request.POST.get('value')

            if field == 'stock':
                product.stock = value
                product.save()
                return JsonResponse({'success': 'Stock updated successfully'})
        except QuickAdd.DoesNotExist:
            return JsonResponse({'error': 'Product not found or you are not authorized'})

    return JsonResponse({'error': 'Invalid request'})


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
