from django.db import models
from django.core.validators import MinValueValidator

class FundAllocation(models.Model):
    DEPARTMENT_CHOICES = (
        ('health', 'Health'),
        ('education', 'Education'),
        ('infrastructure', 'Infrastructure'),
        ('defense', 'Defense'),
        ('agriculture', 'Agriculture'),
        ('welfare', 'Social Welfare'),
        ('other', 'Other'),
    )
    
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    allocated_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    #allocation_date = models.DateField(auto_now_add=True)
    allocation_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    region = models.CharField(max_length=100)
    supporting_document = models.FileField(upload_to='fund_allocations/%Y/%m/%d/', null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-allocation_date']  # Newest first
        verbose_name_plural = "Fund Allocations"
    
    def __str__(self):
        return f"{self.department} - ₹{self.allocated_amount}"
