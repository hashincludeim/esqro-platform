from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('contracts/', views.contracts_view, name='contracts'),
    path('payments/', views.payments_view, name='payments'),
    path('analytics/', views.analytics_view, name='analytics'),
]