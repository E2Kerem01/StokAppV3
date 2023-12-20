from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import login_page, logout_page, contact_page, send_mail

urlpatterns = [
    path('sistem/', login_page, name='sistem'),
    path('logout/', logout_page, name='logout'),
    path('contact/', contact_page, name='contact'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_page, name = 'logout'),

]