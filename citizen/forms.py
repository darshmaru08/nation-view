from django import forms
from .models import TaxSubmission, Feedback

class TaxSubmissionForm(forms.ModelForm):
    class Meta:
        model = TaxSubmission
        fields = ['pan_number', 'financial_year', 'amount_paid', 'payment_mode', 'receipt']
        widgets = {
            'financial_year': forms.TextInput(attrs={'placeholder': 'YYYY-YYYY'}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['subject', 'message']
