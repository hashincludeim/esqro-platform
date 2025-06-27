from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('contracts/', views.contracts_view, name='contracts'),
    path('contracts/create/', views.contract_create, name='contract_create'),
    path('contracts/<uuid:contract_id>/', views.contract_detail, name='contract_detail'),
    path('payments/', views.payments_view, name='payments'),
    path('analytics/', views.analytics_view, name='analytics'),
]