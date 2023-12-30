

from django.urls import path
from .views import create_product, productmanagement, category, quick_sale, quick_sale_page, sales_history, \
    product_sales_history, salesperson_list, create_salesperson, salesperson_detail, SalesPersonDeleteView, \
    SalesPersonUpdateView

urlpatterns = [

    path('createproduct/', create_product, name='createproduct'),
    path('productmanagement/', productmanagement, name='productmanagement'),
    path('category/', category, name='category'),

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
]
