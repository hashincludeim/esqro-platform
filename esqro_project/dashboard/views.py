from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def dashboard_home(request):
    context = {
        'user': request.user,
        'page_title': 'Dashboard',
        'active_nav': 'dashboard'
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def contracts_view(request):
    context = {
        'user': request.user,
        'page_title': 'Contracts',
        'active_nav': 'contracts'
    }
    return render(request, 'dashboard/contracts.html', context)

@login_required
def payments_view(request):
    context = {
        'user': request.user,
        'page_title': 'Payments',
        'active_nav': 'payments'
    }
    return render(request, 'dashboard/payments.html', context)

@login_required
def analytics_view(request):
    context = {
        'user': request.user,
        'page_title': 'Analytics',
        'active_nav': 'analytics'
    }
    return render(request, 'dashboard/analytics.html', context)