import logging

from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ProductForm, CategoryForm, SalesPersonForm, QuickAddForm, UsernameChangeForm
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView
from .forms import ProductForm, CategoryForm, SalesPersonForm
from .models import QuickAdd, SalesPerson, Sales, Payment, Category
from django.db.models import Case, When, F, Value, Sum, BooleanField, IntegerField
from datetime import datetime, timedelta
from django.utils.datetime_safe import date
from django.http import HttpResponse
from decimal import Decimal
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

logger = logging.getLogger(__name__)


class QuickAddUpdate(UpdateView):
    model = QuickAdd
    form_class = QuickAddForm
    template_name = 'store/quickadd.html'
    success_url = reverse_lazy('productmanagement')


@login_required(login_url='sistem')
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


@login_required(login_url='sistem')
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
    query_name = request.GET.get('product_name')
    query_barkod = request.GET.get('product_barkod')

    if query_name:
        user_products = user_products.filter(user=request.user, name__icontains=query_name)
    elif query_barkod:
        user_products = user_products.filter(user=request.user, barkod__icontains=query_barkod)

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
    user_categories = Category.objects.filter(user=request.user)
    if request.method == 'POST':
        forms = CategoryForm(request.POST)
        if forms.is_valid():
            category = forms.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('category')
    context = {
        'form': forms,
        'user_categories': user_categories,
    }
    return render(request, 'store/category.html', context)


# Kullanıcı şifre değiştirme işlemi
@login_required(login_url='sistem')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Oturum kimliği güncellenmeli, aksi halde kullanıcı oturumu kapanabilir
            update_session_auth_hash(request, user)
            logout(request)
            return redirect('password_change_done')  # Şifre değiştirme başarılı olduğunda yönlendirme yap
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'store/change_password.html', {'form': form})


# # Kullanıcı adı değiştirme işlemi
# @login_required(login_url='sistem')
# def change_username(request):
#     if request.method == 'POST':
#         form = UserChangeForm(user=request.user, data=request.POST)
#         if form.is_valid():
#             user = form.save()
#             # Oturum kimliği güncellenmeli, aksi halde kullanıcı oturumu kapanabilir
#             update_session_auth_hash(request, user)
#             logout(request)
#             return redirect('username_change_done')  # Şifre değiştirme başarılı olduğunda yönlendirme yap
#     else:
#         form = UserChangeForm(user=request.user)
#     return render(request, 'store/change_username.html', {'form': form})


# @login_required(login_url='sistem')
# def change_username(request):
#     if request.method == 'POST':
#         form = UserChangeForm(data=request.POST, instance=request.user)
#         if form.is_valid():
#             user = form.save()
#             # Oturum kimliği güncellenmeli, aksi halde kullanıcı oturumu kapanabilir
#             update_session_auth_hash(request, user)
#             return redirect('password_change_done')  # Şifre değiştirme başarılı olduğunda yönlendirme yap
#     else:
#         form = UserChangeForm(instance=request.user)
#     return render(request, 'store/change_username.html', {'form': form})


@login_required(login_url='sistem')
def change_username(request):
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            # Oturum kimliği güncellenmeli, aksi halde kullanıcı oturumu kapanabilir
            update_session_auth_hash(request, user)
            messages.success(request, 'Kullanıcı adı başarıyla değiştirildi.')
            return redirect('dashboard')
    else:
        form = UsernameChangeForm(instance=request.user)
    return render(request, 'store/change_username.html', {'form': form})










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


@login_required(login_url='sistem')
def salesperson_details(request, salesperson_id):
    if request.user.is_authenticated:
        salesperson = get_object_or_404(SalesPerson, id=salesperson_id)

        # Get start and end dates from user input or default to today's date
        start_date_str = request.GET.get('start_date', '')
        end_date_str = request.GET.get('end_date', '')

        today = date.today()

        # Use the consistent 'Y-m-d' format for parsing
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else today
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else today + timedelta(
            days=1)  # Assume end date is inclusive

        sales_table, total_profit_for_person, total_debt = calculate_bor_kutusu_salesdetails(salesperson, start_date,
                                                                                             end_date)

        context = {
            'sales_table': sales_table,
            'salesperson': salesperson,
            'salesperson_id': salesperson_id,
            'total_debt': total_debt,
            'currency': 'USD',
            'total_profit_for_person': total_profit_for_person, }
    else:
        return redirect('login')

    return render(request, 'store/rapor_cari.html', context)


def calculate_bor_kutusu_salesdetails(salesperson, start_date, end_date):
    sales_table = []

    sales_info = Sales.objects.filter(
        Q(sold_by=salesperson) & Q(date_sold__range=(start_date, end_date)) |
        Q(sold_by=salesperson, is_credit=False, date_sold__range=(start_date, end_date)),
    )

    for sale in sales_info:
        sales_table.append({
            'salesperson_name': salesperson.name,
            'borca': sale.is_credit,
            'product_name': sale.product.name,
            'quantity_sold': sale.quantity_sold,
            'sale_amount': (sale.product.satisFiyati) * sale.quantity_sold,
            'product_price': sale.product.maaliyet,
            'product_sold_price': sale.product.satisFiyati,
            'sold_date': sale.date_sold,
            'sales_person_tel': salesperson.phone_number,
        })

    # Ödemeleri ekleyin
    payments = Payment.objects.filter(salesperson=salesperson, date_paid__range=(start_date, end_date))
    for payment in payments:
        sales_table.append({
            'salesperson_name': salesperson.name,
            'borca': False,
            'product_name': 'ÖDEME(Nakit)',
            'quantity_sold': '-',
            'sale_amount': '-' + str(payment.amount),
            'product_price': '-',
            'product_sold_price': '-',
            'sold_date': payment.date_paid,
            'sales_person_tel': salesperson.phone_number,
        })

    total_profit_for_person = SalesPerson.objects.filter(id=salesperson.id).annotate(
        total_profit_for_person=Sum(
            (F('sales_by_person__product__satisFiyati') - F('sales_by_person__product__maaliyet')) * F(
                'sales_by_person__quantity_sold'))
    ).first()

    # total_profit_for_person'ı Decimal nesnesinden alınan değere dönüştürün
    total_profit_for_person_value = total_profit_for_person.total_profit_for_person if total_profit_for_person else Decimal(
        '0.0')

    return sales_table, total_profit_for_person_value, salesperson.debt


@login_required(login_url='sistem')
class SalesPersonDeleteView(DeleteView):
    model = SalesPerson
    template_name = 'store/salesperson_confirm_delete.html'
    success_url = reverse_lazy('salesperson_list')


class SalesPersonUpdateView(UpdateView):
    model = SalesPerson
    form_class = SalesPersonForm
    template_name = 'store/salesperson_form.html'
    success_url = reverse_lazy('salesperson_list')


@login_required(login_url='sistem')
def update_salesperson_(request, pk):
    salesperson = get_object_or_404(SalesPerson, pk=pk)

    if request.method == 'POST':
        form = SalesPersonForm(request.POST, instance=salesperson)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('salesperson_detail', args=[pk]))
    else:
        form = SalesPersonForm(instance=salesperson)

    return render(request, 'store/salesperson_update.html', {'form': form, 'salesperson': salesperson})


from django.db.models import Q


@login_required(login_url='sistem')
def salesperson_list(request):
    query = request.GET.get('q')
    salespeople_list = SalesPerson.objects.all()

    if query:
        salespeople_list = salespeople_list.filter(
            Q(name__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(debt__icontains=query)
        )

    # Number of salespeople to display per page
    items_per_page = 5
    paginator = Paginator(salespeople_list, items_per_page)

    page = request.GET.get('page')
    try:
        salespeople = paginator.page(page)
    except PageNotAnInteger:
        salespeople = paginator.page(1)
    except EmptyPage:
        salespeople = paginator.page(paginator.num_pages)

    return render(request, 'store/salesperson_list.html', {'salespeople': salespeople, 'query': query})


@login_required(login_url='sistem')
def create_salesperson(request):
    if request.method == 'POST':
        form = SalesPersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salesperson_list')
    else:
        form = SalesPersonForm()

    return render(request, 'store/salesperson_form.html', {'form': form})


@login_required(login_url='sistem')
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

@login_required(login_url='sistem')
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


@login_required(login_url='sistem')
def sales_history(request):
    sales = Sales.objects.filter(sold_to=request.user)
    return render(request, 'store/sales_history.html', {'sales': sales})


def calculate_profit_margin(product):
    return product.satisFiyati - product.maaliyet


def update_total_profit_margin(total_profit_margin, profit_margin):
    return total_profit_margin + profit_margin


@login_required(login_url='sistem')
def quick_sale_page(request):
    total_profit_margin = 0
    search_term = request.GET.get('search', '')

    if request.user.is_authenticated:
        if search_term:
            products = QuickAdd.objects.filter(user=request.user, name__icontains=search_term)
        else:
            products = QuickAdd.objects.none()

        product_count = products.count()

        salespeople = SalesPerson.objects.all()

        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            quantity_sold = int(request.POST.get('quantity_sold'))
            sold_by_id = request.POST.get('sold_by')
            is_credit = request.POST.get('isCredit') == 'True'
            print("Is Credit (raw):", request.POST.get('isCredit'))
            print("Is Credit (boolean):", is_credit)

            product = QuickAdd.objects.get(id=product_id)

            if product.stock >= quantity_sold:
                product.stock -= quantity_sold
                product.save()

                # QuickAdd nesnesini kaydet
                product.save()

                profit_margin = calculate_profit_margin(product) * quantity_sold
                total_profit_margin = update_total_profit_margin(total_profit_margin, profit_margin)

                sold_by = SalesPerson.objects.get(id=sold_by_id)

                sales = Sales.objects.create(
                    product=product,
                    quantity_sold=quantity_sold,
                    sold_to=request.user,
                    sold_by=sold_by,
                    is_credit=is_credit
                )

                if sales.is_credit and product.satisFiyati * quantity_sold > 0:
                    sold_by.debt += product.satisFiyati * quantity_sold
                    sold_by.save()

                messages.success(request, 'Satış başarıyla kaydedildi.')
            else:
                messages.error(request, 'Yetersiz stok')

        sales_history = Sales.objects.filter(product__user=request.user)

        return render(request, 'store/sales.html', {
            'products': products,
            'product_count': product_count,
            'search_term': search_term,
            'total_profit_margin': total_profit_margin,
            'sales_history': sales_history,
            'salespeople': salespeople
        })
    else:
        return redirect('login')


@login_required(login_url='login')
def credit_sales_page(request):
    if request.user.is_authenticated:
        salespeople = SalesPerson.objects.all()

        # Get start and end dates from user input or default to today's date
        start_date_str = request.GET.get('start_date', '')
        end_date_str = request.GET.get('end_date', '')

        today = date.today()

        # Use the consistent 'Y-m-d' format for parsing
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else today
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else today + timedelta(
            days=1)  # Assume end date is inclusive

        # Bor kutusu bilgisini hesapla
        bor_kutusu_bilgisi, sales_table, total_profit_for_person = calculate_bor_kutusu(start_date, end_date)

        """   # Sayfalandırma işlemi
        items_per_page = 10
        paginator = Paginator(sales_table, items_per_page)

        page = request.GET.get('page')

        try:
            sales_table = paginator.page(page)
        except PageNotAnInteger:
            sales_table = paginator.page(1)
        except EmptyPage:
            sales_table = paginator.page(paginator.num_pages)"""

        # salesperson.debt = salesperson.total_sales
        return render(request, 'store/credit_sales.html', {
            'salespeople': salespeople,
            'total_profit_for_person': total_profit_for_person,
            'sales_table': sales_table,
            'bor_kutusu_bilgisi': bor_kutusu_bilgisi,
            'start_date': start_date_str if start_date_str else today.strftime('%Y-%m-%d'),
            'end_date': end_date_str if end_date_str else (today + timedelta(days=1)).strftime('%Y-%m-%d'),
            # Assume end date is inclusive
        })
    else:
        return redirect('login')


def calculate_bor_kutusu(start_date, end_date):
    # Toplam Borcu hesaplama bölümü
    total_sales = SalesPerson.objects.annotate(
        total_sales=Sum(
            Case(
                # When(sales_by_person__is_credit=True, then=F('sales_by_person__quantity_sold') * (F('sales_by_person__product__satisFiyati') - F('sales_by_person__product__maaliyet'))),
                When(sales_by_person__is_credit=True,
                     then=F('sales_by_person__quantity_sold') * F('sales_by_person__product__satisFiyati')),
                default=Value(0),
                output_field=IntegerField(),
            )
        )
    )
    total_profit_for_person = SalesPerson.objects.annotate(
        total_profit_for_person=Sum(
            (F('sales_by_person__product__satisFiyati') - F('sales_by_person__product__maaliyet')) * F(
                'sales_by_person__quantity_sold'))
    )

    bor_kutusu_bilgisi = ''
    sales_table = []

    for idx, salesperson in enumerate(total_sales):

        bor_kutusu_bilgisi += f"{salesperson.name} için Borç: {salesperson.debt}, Toplam Satış: {salesperson.total_sales}, Toplam Kar: {total_profit_for_person[idx].total_profit_for_person}<br>"

        sales_info = Sales.objects.filter(
            sold_by=salesperson,
            date_sold__range=(start_date, end_date)
        )
        for sale in sales_info:
            sales_table.append({
                'salesperson_name': salesperson.name,
                'borca': sale.is_credit,
                'product_name': sale.product.name,
                'quantity_sold': sale.quantity_sold,
                'sale_amount': (sale.product.satisFiyati - sale.product.maaliyet) * sale.quantity_sold,
                'product_price': sale.product.maaliyet,
                'product_sold_price': sale.product.satisFiyati,
                'sold_date': sale.date_sold,
                'sales_person_tel': salesperson.phone_number,
            })

    return bor_kutusu_bilgisi, sales_table, total_profit_for_person


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required(login_url='sistem')
def cast_page(request):
    if request.user.is_authenticated:
        salespeople = SalesPerson.objects.all()

        # Get start and end dates from user input or default to today's date
        start_date_str = request.GET.get('start_date', '')
        end_date_str = request.GET.get('end_date', '')

        today = date.today()

        # Use the consistent 'Y-m-d' format for parsing
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else today
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else today + timedelta(
            days=1)  # Assume end date is inclusive

        # Bor kutusu bilgisini hesapla
        bor_kutusu_bilgisi, sales_table, total_profit_for_person = calculate_bor_kutusu(start_date, end_date)

        # Toplam borcu olan kişilerin toplam borcunu hesapla
        total_debt = sum(salesperson.debt for salesperson in salespeople)
        total_debt = float(total_debt)

        return render(request, 'store/cast.html', {
            'salespeople': salespeople,
            'total_profit_for_person': total_profit_for_person,
            'sales_table': sales_table,
            'bor_kutusu_bilgisi': bor_kutusu_bilgisi,
            'start_date': start_date_str if start_date_str else today.strftime('%Y-%m-%d'),
            'end_date': end_date_str if end_date_str else (today + timedelta(days=1)).strftime('%Y-%m-%d'),
            # Assume end date is inclusive
            'total_debt': total_debt,
        })
    else:
        return redirect('login')


@login_required(login_url='sistem')
def update_debt(request, salesperson_id):
    if request.user.is_authenticated and request.method == 'POST':
        salesperson = get_object_or_404(SalesPerson, id=salesperson_id)
        payment_amount_str = request.POST.get('payment_amount', '0')

        try:
            payment_amount = Decimal(payment_amount_str)
        except ValueError:
            return HttpResponse('Invalid Payment Amount', status=400)

        if payment_amount > 0:
            # Ödeme yapılırken Payment modeline kaydedilebilir
            payment = Payment.objects.create(
                salesperson=salesperson,
                amount=payment_amount,
                date_paid=datetime.now(),  # İsterseniz gerçek tarih bilgisini ekleyebilirsiniz
            )

            salesperson.debt -= payment_amount
            salesperson.save()

        return redirect('cast_page')

    return HttpResponse('Bad Request', status=400)


@login_required(login_url='sistem')
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


from django.views.generic import View
import logging
from django.db import transaction
import pandas as pd

logger = logging.getLogger(__name__)


class ExcelProcessorView(View):
    template_name = 'excel_processor.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if 'excel_file' in request.FILES:
            excel_file = request.FILES['excel_file']
            try:
                # Read Excel file
                df = pd.read_excel(excel_file)

                # Process DataFrame and update the database
                data_list = df.to_dict(orient='records')

                with transaction.atomic():
                    # Clear existing data in the database
                    QuickAdd.objects.all().delete()

                    # Create new records based on the Excel data
                    for excel_row in data_list:
                        excel_row['user'] = request.user
                        QuickAdd.objects.create(**excel_row)

                # Log success
                logger.info(f"Excel file processed successfully: {excel_file.name}")

                # Send a success response
                return JsonResponse({'success': True, 'message': 'Veriler başarıyla işlendi.'})

            except Exception as e:
                # Log the error
                logger.error(f"Error processing Excel file: {e}")

                # Send an error response
                return JsonResponse({'success': False, 'message': 'Veriler basariyla islendi.'})
        else:
            # Send an error response if no file is provided
            return JsonResponse({'success': False, 'message': 'Dosya gönderilmedi.'})


class ExportToExcelView(View):
    def get(self, request, *args, **kwargs):
        # Get data from the database
        data = QuickAdd.objects.all().values()

        # Create a DataFrame from the database data
        df = pd.DataFrame.from_records(data)

        # Convert datetime columns to timezone-unaware datetimes
        df['created_day'] = df['created_day'].dt.tz_localize(None)

        # Create a response with the Excel file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=YEDEK_DOSYASI.xlsx'

        # Write the DataFrame to the response
        df.to_excel(response, index=False, engine='xlsxwriter')

        return response


@login_required(login_url='login')
def backup_data_view(request):
    return render(request, 'store/yedekleme.html')
