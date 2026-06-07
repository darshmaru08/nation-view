from django import forms
from .models import FundAllocation

class FundAllocationForm(forms.ModelForm):
    class Meta:
        model = FundAllocation
        fields = ['department', 'allocated_amount', 'description', 'region', 'supporting_document']
