from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from .forms import CustomLoginForm

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get(self, request, *args, **kwargs):
        # Clear any existing messages when displaying login page
        storage = messages.get_messages(request)
        storage.used = True
        return super().get(request, *args, **kwargs)
    
    def get_success_url(self):
        # Check if user has a specific redirect URL
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        # Default to dashboard
        return reverse('dashboard:home')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)

def custom_logout(request):
    logout(request)
    return redirect('landing:index')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})