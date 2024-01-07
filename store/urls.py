

from django.urls import path
from .views import create_product, productmanagement, category, quick_sale, quick_sale_page, sales_history, \
    product_sales_history, salesperson_list, create_salesperson, salesperson_detail, SalesPersonDeleteView, \
    SalesPersonUpdateView, QuickAddUpdate, update_product, update_salesperson_, credit_sales_page, cast_page, \
    update_debt,salesperson_details

urlpatterns = [

    path('createproduct/', create_product, name='createproduct'),
    path('productmanagement/', productmanagement, name='productmanagement'),
    path('category/', category, name='category'),
     #path('products/', product_list, name='product_list'),
    path('update_product/<int:pk>/', update_product, name='update_product'),

    # MEHMET PATH

    path('quicksale/', quick_sale, name='quicksale'),
    path('quicksalepage/', quick_sale_page, name='quicksalepage'),  # Yeni eklenen satış sayfası URL'si
    path('sales/', sales_history, name='sales_history'),
    path('urun_satıs_gecmisi/<int:product_id>/', product_sales_history, name='product_sales_history'),
    path('salesperson/', salesperson_list, name='salesperson_list'),
    path('salesperson/create/', create_salesperson, name='create_salesperson'),
    path('salesperson/<int:pk>/', salesperson_detail, name='salesperson_detail'),
    path('salesperson/<int:pk>/delete/', SalesPersonDeleteView.as_view(), name='delete_salesperson'),
    path('salesperson/<int:pk>/update/', SalesPersonUpdateView.as_view(), name='update_salesperson'),


    # MEHMET PATH

    path('update_salesperson/<int:pk>/', update_salesperson_, name='update_salesperson'),
    path('credit_sales/', credit_sales_page, name='credit_sales_page'),
    path('cast/', cast_page, name='cast_page'),
    path('update_debt/<int:salesperson_id>/', update_debt, name='update_debt'),
    path('salesperson-details/<int:salesperson_id>/', salesperson_details, name='salesperson_details'),


]
