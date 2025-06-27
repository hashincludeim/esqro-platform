from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Contract, ContractMilestone
from .forms import ContractCreateForm, ContractMilestoneForm
from datetime import date, timedelta

@login_required
def dashboard_home(request):
    user_contracts = Contract.objects.filter(contractor=request.user)
    
    # Calculate statistics
    total_contracts = user_contracts.count()
    active_contracts = user_contracts.filter(status='active').count()
    completed_contracts = user_contracts.filter(status='completed').count()
    pending_contracts = user_contracts.filter(status='pending').count()
    
    # Calculate total values
    total_value = user_contracts.aggregate(Sum('total_value'))['total_value__sum'] or 0
    escrow_total = sum(contract.escrow_amount for contract in user_contracts.filter(status__in=['active', 'pending']))
    
    # Recent contracts
    recent_contracts = user_contracts.order_by('-created_at')[:5]
    
    context = {
        'user': request.user,
        'page_title': 'Dashboard',
        'active_nav': 'dashboard',
        'stats': {
            'total_contracts': total_contracts,
            'active_contracts': active_contracts,
            'completed_contracts': completed_contracts,
            'pending_contracts': pending_contracts,
            'total_value': total_value,
            'escrow_total': escrow_total,
        },
        'recent_contracts': recent_contracts,
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def contracts_view(request):
    contracts = Contract.objects.filter(contractor=request.user).order_by('-created_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter and status_filter != 'all':
        contracts = contracts.filter(status=status_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        contracts = contracts.filter(
            Q(title__icontains=search_query) |
            Q(contract_number__icontains=search_query) |
            Q(client_name__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(contracts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'user': request.user,
        'page_title': 'Contracts',
        'active_nav': 'contracts',
        'contracts': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    return render(request, 'dashboard/contracts.html', context)

@login_required
def contract_create(request):
    if request.method == 'POST':
        form = ContractCreateForm(request.POST, request.FILES)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.contractor = request.user
            contract.save()
            messages.success(request, f'Contract {contract.contract_number} created successfully!')
            return redirect('dashboard:contract_detail', contract_id=contract.id)
    else:
        form = ContractCreateForm()
    
    context = {
        'user': request.user,
        'page_title': 'Create Contract',
        'active_nav': 'contracts',
        'form': form,
    }
    return render(request, 'dashboard/contract_create.html', context)

@login_required
def contract_detail(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id, contractor=request.user)
    milestones = contract.milestones.all()
    
    context = {
        'user': request.user,
        'page_title': f'Contract {contract.contract_number}',
        'active_nav': 'contracts',
        'contract': contract,
        'milestones': milestones,
    }
    return render(request, 'dashboard/contract_detail.html', context)

@login_required
def payments_view(request):
    # Get all milestones for user's contracts that involve payments
    milestones = ContractMilestone.objects.filter(
        contract__contractor=request.user
    ).select_related('contract').order_by('-created_at')
    
    # Calculate payment statistics
    total_milestones = milestones.count()
    completed_payments = milestones.filter(status='completed').count()
    pending_payments = milestones.filter(status='pending').count()
    total_payment_value = milestones.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
    
    context = {
        'user': request.user,
        'page_title': 'Payments',
        'active_nav': 'payments',
        'milestones': milestones[:10],  # Show latest 10
        'stats': {
            'total_milestones': total_milestones,
            'completed_payments': completed_payments,
            'pending_payments': pending_payments,
            'total_payment_value': total_payment_value,
        }
    }
    return render(request, 'dashboard/payments.html', context)

@login_required
def analytics_view(request):
    user_contracts = Contract.objects.filter(contractor=request.user)
    
    # Analytics data
    contracts_by_status = {
        'active': user_contracts.filter(status='active').count(),
        'completed': user_contracts.filter(status='completed').count(),
        'pending': user_contracts.filter(status='pending').count(),
        'draft': user_contracts.filter(status='draft').count(),
    }
    
    contracts_by_type = {}
    for contract_type, _ in Contract.CONTRACT_TYPE_CHOICES:
        contracts_by_type[contract_type] = user_contracts.filter(contract_type=contract_type).count()
    
    # Monthly contract creation
    monthly_data = []
    for i in range(12):
        month_start = date.today().replace(day=1) - timedelta(days=30*i)
        month_contracts = user_contracts.filter(
            created_at__year=month_start.year,
            created_at__month=month_start.month
        ).count()
        monthly_data.append({
            'month': month_start.strftime('%b %Y'),
            'count': month_contracts
        })
    
    context = {
        'user': request.user,
        'page_title': 'Analytics',
        'active_nav': 'analytics',
        'contracts_by_status': contracts_by_status,
        'contracts_by_type': contracts_by_type,
        'monthly_data': monthly_data[:6],  # Last 6 months
    }
    return render(request, 'dashboard/analytics.html', context)