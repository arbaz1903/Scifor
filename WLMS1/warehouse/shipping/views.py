from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def shipment_list(request):
    return render(request, 'shipping/shipment_list.html', {})