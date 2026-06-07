from django.db import models
from django.core.validators import MinValueValidator
from core.models import User

class TaxSubmission(models.Model):
    PAYMENT_MODES = (
        ('online', 'Online Payment'),
        ('cheque', 'Cheque'),
        ('cash', 'Cash'),
        ('other', 'Other'),
        
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pan_number = models.CharField(max_length=10)
    financial_year = models.CharField(max_length=9)  # Format: 2023-2024
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODES)
    receipt = models.FileField(upload_to='tax_receipts/')
    submission_date = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.financial_year} - ₹{self.amount_paid}"


   

        
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True)
    responded = models.BooleanField(default=False)
    
    def __str__(self):
        return self.subject
