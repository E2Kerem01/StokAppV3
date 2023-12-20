from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from store.models import QuickAdd


@login_required(login_url='sistem')
def dashboard(request):
    user_products = QuickAdd.objects.filter(user=request.user)
    product_count = user_products.count()
    return render(request, 'dashboard.html', {'product_count': product_count})

