from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
import uuid
import os

User = get_user_model()

def contract_document_path(instance, filename):
    """Generate file path for contract documents"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('contracts', str(instance.id), filename)

class Contract(models.Model):
    CONTRACT_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('overdue', 'Overdue'),
    ]
    
    CONTRACT_TYPE_CHOICES = [
        ('construction', 'Construction'),
        ('infrastructure', 'Infrastructure'),
        ('commercial', 'Commercial'),
        ('residential', 'Residential'),
        ('renovation', 'Renovation'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contract_number = models.CharField(max_length=50, unique=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    contract_type = models.CharField(max_length=20, choices=CONTRACT_TYPE_CHOICES, default='construction')
    
    # Parties
    contractor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contractor_contracts')
    client_name = models.CharField(max_length=255)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=20, blank=True)
    client_company = models.CharField(max_length=255, blank=True)
    
    # Financial Details
    total_value = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default='QAR')
    escrow_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=100.00, 
                                         help_text="Percentage of total value to be held in escrow")
    
    # Timeline
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Status and Progress
    status = models.CharField(max_length=20, choices=CONTRACT_STATUS_CHOICES, default='draft')
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Documents
    contract_document = models.FileField(upload_to=contract_document_path, blank=True, null=True)
    
    # Location
    project_location = models.CharField(max_length=500, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts'
    
    def __str__(self):
        return f"{self.contract_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.contract_number:
            # Generate contract number: CON-YYYY-NNNN
            from datetime import datetime
            year = datetime.now().year
            last_contract = Contract.objects.filter(
                contract_number__startswith=f'CON-{year}-'
            ).order_by('-contract_number').first()
            
            if last_contract:
                last_number = int(last_contract.contract_number.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.contract_number = f'CON-{year}-{new_number:04d}'
        
        super().save(*args, **kwargs)
    
    @property
    def escrow_amount(self):
        """Calculate the amount to be held in escrow"""
        return (self.total_value * self.escrow_percentage) / 100
    
    @property
    def is_overdue(self):
        """Check if contract is overdue"""
        from datetime import date
        return self.end_date < date.today() and self.status == 'active'

class ContractMilestone(models.Model):
    MILESTONE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    payment_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=MILESTONE_STATUS_CHOICES, default='pending')
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['due_date']
    
    def __str__(self):
        return f"{self.contract.contract_number} - {self.title}"

class ContractDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('contract', 'Main Contract'),
        ('amendment', 'Amendment'),
        ('invoice', 'Invoice'),
        ('receipt', 'Receipt'),
        ('permit', 'Permit'),
        ('certificate', 'Certificate'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, default='other')
    file = models.FileField(upload_to=contract_document_path)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.PositiveIntegerField(blank=True, null=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.contract.contract_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)
# Create your models here.
