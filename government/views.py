from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FundAllocationForm
from .models import FundAllocation
from citizen.models import TaxSubmission
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum


@login_required
@login_required
def allocate_funds(request):
    if request.user.role != 'government':
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = FundAllocationForm(request.POST, request.FILES)
        if form.is_valid():
            # Calculate available funds
            total_tax = TaxSubmission.objects.filter(verified=True).aggregate(
                Sum('amount_paid'))['amount_paid__sum'] or 0
            total_allocated = FundAllocation.objects.aggregate(
                Sum('allocated_amount'))['allocated_amount__sum'] or 0
            available_funds = total_tax - total_allocated
            
            # Check if allocation exceeds available funds
            allocation_amount = form.cleaned_data['allocated_amount']
            if allocation_amount > available_funds:
                messages.error(request, 
                    f"Insufficient funds. Available: ₹{available_funds:,.2f}")
                return render(request, 'government/allocate_funds.html', 
                           {'form': form})
            
            # Save if funds are available
            allocation = form.save()
            messages.success(request, 
                f"₹{allocation.allocated_amount:,.2f} allocated to {allocation.sector}")
            return redirect('fund_tracker')  # Redirect to fund tracker instead
            
    else:
        form = FundAllocationForm()
    
    # Show available funds on GET request
    total_tax = TaxSubmission.objects.filter(verified=True).aggregate(
        Sum('amount_paid'))['amount_paid__sum'] or 0
    total_allocated = FundAllocation.objects.aggregate(
        Sum('allocated_amount'))['allocated_amount__sum'] or 0
    
    return render(request, 'government/allocate_funds.html', {
        'form': form,
        'available_funds': total_tax - total_allocated,
        'total_tax': total_tax,
        'total_allocated': total_allocated
    })
# def allocate_funds(request):
#     if request.user.role != 'government':
#         return redirect('dashboard')
        
#     if request.method == 'POST':
#         form = FundAllocationForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('tax_reports')
#     else:
#         form = FundAllocationForm()
#     return render(request, 'government/allocate_funds.html', {'form': form})

@login_required
def tax_reports(request):
    if request.user.role != 'government':
        return redirect('dashboard')
        
    tax_submissions = TaxSubmission.objects.filter(verified=True)
    allocations = FundAllocation.objects.all()
    
    context = {
        'tax_submissions': tax_submissions,
        'allocations': allocations,
        'total_tax': sum([t.amount_paid for t in tax_submissions]),
        'total_allocated': sum([a.allocated_amount for a in allocations]),
    }
    return render(request, 'government/tax_reports.html', context)

from django.contrib import messages
from citizen.models import TaxSubmission

# @login_required
# @user_passes_test(lambda u: u.role == 'government')
# def verify_taxes(request):
#     if request.method == 'POST':
#         tax_id = request.POST.get('tax_id')
#         action = request.POST.get('action')
        
#         tax = TaxSubmission.objects.get(id=tax_id)
#         if action == 'verify':
#             tax.verified = True
#             messages.success(request, f'Tax #{tax_id} verified')
#         elif action == 'reject':
#             tax.delete()
#             messages.warning(request, f'Tax #{tax_id} rejected')
#         tax.save()
#         return redirect('verify_taxes')
    
#     unverified_taxes = TaxSubmission.objects.filter(verified=False)
#     return render(request, 'government/verify_taxes.html', {
#         'taxes': unverified_taxes
#     })


@login_required
@user_passes_test(lambda u: u.role == 'government')
def verify_taxes(request):
    if request.method == 'POST':
        tax_id = request.POST.get('tax_id')
        action = request.POST.get('action')
        
        try:
            tax = TaxSubmission.objects.get(id=tax_id)
            if action == 'verify':
                tax.verified = True
                messages.success(request, f'Tax #{tax_id} verified')
            elif action == 'reject':
                tax.delete()
                messages.warning(request, f'Tax #{tax_id} rejected')
            tax.save()
        except TaxSubmission.DoesNotExist:
            messages.error(request, 'Tax submission not found')
        
        return redirect('verify_taxes')
    
    unverified_taxes = TaxSubmission.objects.filter(verified=False)
    return render(request, 'government/verify_taxes.html', {
        'taxes': unverified_taxes
    })

@login_required
def fund_tracker(request):
    if request.user.role != 'government':
        return redirect('dashboard')
    
    allocations = FundAllocation.objects.all().order_by('-allocation_date')
    
    # Calculate summary statistics
    total_allocated = allocations.aggregate(Sum('allocated_amount'))['allocated_amount__sum'] or 0
    approved_amount = allocations.filter(is_approved=True).aggregate(Sum('allocated_amount'))['allocated_amount__sum'] or 0
    
    context = {
        'allocations': allocations,
        'total_allocated': total_allocated,
        'approved_amount': approved_amount,
        'pending_amount': total_allocated - approved_amount,
    }
    return render(request, 'government/fund_tracker.html', context)

@login_required
def approve_allocation(request, pk):
    if request.user.role != 'government':
        return redirect('dashboard')
    
    allocation = get_object_or_404(FundAllocation, pk=pk)
    allocation.is_approved = True
    allocation.save()
    
    messages.success(request, f"Allocation #{pk} approved successfully")
    return redirect('fund_tracker')