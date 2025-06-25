from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'company_name', 'is_contractor', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_contractor', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'company_name')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Company Information', {
            'fields': ('company_name', 'phone_number', 'is_contractor')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Company Information', {
            'fields': ('email', 'company_name', 'phone_number', 'is_contractor')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('date_joined',)
        return self.readonly_fields