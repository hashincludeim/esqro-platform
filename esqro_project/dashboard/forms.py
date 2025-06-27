from django import forms
from django.core.validators import FileExtensionValidator
from .models import Contract, ContractMilestone, ContractDocument

class ContractCreateForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = [
            'title', 'description', 'contract_type', 'client_name', 
            'client_email', 'client_phone', 'client_company', 'total_value',
            'escrow_percentage', 'start_date', 'end_date', 'project_location',
            'contract_document'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter contract title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the project scope and details'
            }),
            'contract_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'client_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full name of the client'
            }),
            'client_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'client@example.com'
            }),
            'client_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+974 XXXX XXXX'
            }),
            'client_company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Client company name (optional)'
            }),
            'total_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'escrow_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '100.00',
                'step': '0.01',
                'min': '0',
                'max': '100'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'project_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Project address or location'
            }),
            'contract_document': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contract_document'].validators.append(
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])
        )
        self.fields['contract_document'].help_text = "Upload contract document (PDF, DOC, DOCX only, max 10MB)"
    
    def clean_contract_document(self):
        file = self.cleaned_data.get('contract_document')
        if file:
            if file.size > 10 * 1024 * 1024:  # 10MB limit
                raise forms.ValidationError("File size cannot exceed 10MB.")
        return file
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("End date must be after start date.")
        
        return cleaned_data

class ContractMilestoneForm(forms.ModelForm):
    class Meta:
        model = ContractMilestone
        fields = ['title', 'description', 'due_date', 'payment_amount']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Milestone title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Milestone description'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'payment_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            })
        }