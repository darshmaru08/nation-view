from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TaxSubmissionForm, FeedbackForm
from .models import TaxSubmission, Feedback

@login_required
def submit_tax(request):
    if request.method == 'POST':
        form = TaxSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            tax_submission = form.save(commit=False)
            tax_submission.user = request.user
            
            # Auto-verify condition (example: auto-verify online payments)
            if tax_submission.payment_mode == 'online':
                tax_submission.verified = True
            
            tax_submission.save()
            
            # Send notification if manual verification needed
            if not tax_submission.verified:
                from django.core.mail import mail_admins
                mail_admins(
                    f'Tax Verification Needed: {tax_submission.pan_number}',
                    f'Amount: ₹{tax_submission.amount_paid}\nMode: {tax_submission.payment_mode}'
                )
            
            return redirect('my_taxes')
    else:
        initial = {
            'pan_number': request.user.pan_number,
            'financial_year': '2023-2024'  # Default value
        }
        form = TaxSubmissionForm(initial=initial)
    return render(request, 'citizen/submit_tax.html', {'form': form})


@login_required
def my_taxes(request):
    tax_submissions = TaxSubmission.objects.filter(user=request.user)
    return render(request, 'citizen/my_taxes.html', {'tax_submissions': tax_submissions})

@login_required
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('dashboard')
    else:
        form = FeedbackForm()
    return render(request, 'citizen/feedback.html', {'form': form})

