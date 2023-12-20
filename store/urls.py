from django.urls import path
from .views import quickadd, create_product

urlpatterns = [
    path('quickadd/', quickadd, name='quickadd'),
    path('createproduct/', create_product, name='createproduct'),
]
