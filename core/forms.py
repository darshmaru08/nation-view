from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import User

class CustomUserCreationForm(UserCreationForm):
    pan_number = forms.CharField(max_length=10, required=False)
    department = forms.CharField(max_length=100, required=False)
    region = forms.CharField(max_length=100, required=False)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('role', 'pan_number', 'department', 'region')
