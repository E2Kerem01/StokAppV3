import logging
import string

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from .forms import QuickAddForm, ProductForm

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


@login_required(login_url='login')
def quickadd(request):
    if request.method == 'POST':
        form = QuickAddForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user  # Oluşturan kullanıcıyı atama
            product.save()
            return render(request, 'dashboard.html', {'form': QuickAddForm()})
    else:
        form = QuickAddForm()

    context = {'form': form}
    return render(request, 'dashboard.html', context)


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