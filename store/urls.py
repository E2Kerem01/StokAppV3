

from django.urls import path
from .views import  create_product, productmanagement, category

urlpatterns = [

    path('createproduct/', create_product, name='createproduct'),
    path('productmanagement/', productmanagement, name='productmanagement'),
    path('category/', category, name='category'),
]
