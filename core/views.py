from django.contrib.auth import logout 
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from citizen.models import TaxSubmission
from government.models import FundAllocation
from core.models import SuccessStory

def home(request):
    return render(request, 'core/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.role == 'citizen':
        tax_submissions = TaxSubmission.objects.filter(user=request.user)
        context = {
            'tax_submissions': tax_submissions,
            'total_contribution': sum([t.amount_paid for t in tax_submissions]),
        }
    else:
        allocations = FundAllocation.objects.all()
        total_tax = sum([t.amount_paid for t in TaxSubmission.objects.filter(verified=True)])
        context = {
            'allocations': allocations,
            'total_tax': total_tax,
        }
    return render(request, 'core/dashboard.html', context)

def fund_tracker(request):
    allocations = FundAllocation.objects.all()
    total_allocated = sum([a.allocated_amount for a in allocations])
    stories = SuccessStory.objects.filter(is_featured=True)
    
    context = {
        'allocations': allocations,
        'total_allocated': total_allocated,
        'stories': stories,
    }
    return render(request, 'core/fund_tracker.html', context)

def success_stories(request):
    stories = SuccessStory.objects.all()
    return render(request, 'core/success_stories.html', {'stories': stories})


def custom_logout(request):
    logout(request)
    return redirect('home')  # Make sure 'home' is the name of your home URL pattern
