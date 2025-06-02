from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required
def order_list(request):
    return render(request, 'orders/order_list.html', {})