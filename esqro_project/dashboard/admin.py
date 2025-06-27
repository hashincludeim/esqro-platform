from django.contrib import admin
from .models import Contract, ContractMilestone, ContractDocument

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['contract_number', 'title', 'contractor', 'client_name', 'total_value', 'status', 'created_at']
    list_filter = ['status', 'contract_type', 'created_at']
    search_fields = ['contract_number', 'title', 'client_name', 'contractor__username']
    readonly_fields = ['contract_number', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('contract_number', 'title', 'description', 'contract_type', 'contract_document')
        }),
        ('Parties', {
            'fields': ('contractor', 'client_name', 'client_email', 'client_phone', 'client_company')
        }),
        ('Financial Details', {
            'fields': ('total_value', 'currency', 'escrow_percentage')
        }),
        ('Timeline & Status', {
            'fields': ('start_date', 'end_date', 'status', 'progress_percentage')
        }),
        ('Location', {
            'fields': ('project_location',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(ContractMilestone)
class ContractMilestoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'contract', 'due_date', 'payment_amount', 'status', 'completion_percentage']
    list_filter = ['status', 'due_date', 'contract__status']
    search_fields = ['title', 'contract__contract_number', 'contract__title']
    ordering = ['due_date']

@admin.register(ContractDocument)
class ContractDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'contract', 'document_type', 'uploaded_by', 'uploaded_at', 'file_size']
    list_filter = ['document_type', 'uploaded_at']
    search_fields = ['title', 'contract__contract_number']
    ordering = ['-uploaded_at']