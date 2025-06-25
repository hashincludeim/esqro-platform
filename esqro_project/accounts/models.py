from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_contractor = models.BooleanField(default=True)
    
    # Remove created_at and updated_at since AbstractUser already has date_joined
    # and we can use auto_now for updates if needed
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def get_display_name(self):
        if self.company_name:
            return self.company_name
        elif self.get_full_name():
            return self.get_full_name()
        else:
            return self.username