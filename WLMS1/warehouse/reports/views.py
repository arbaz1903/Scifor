from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def report_list(request):
    return render(request, 'reports/report_list.html', {})