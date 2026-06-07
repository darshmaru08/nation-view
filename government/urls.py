from django.urls import path
from . import views
from .views import verify_taxes

urlpatterns = [
    path('verify-taxes/', verify_taxes, name='verify_taxes'),
    path('verify-taxes/', verify_taxes, name='verify_taxes'),
    path('allocate-funds/', views.allocate_funds, name='allocate_funds'),
    path('tax-reports/', views.tax_reports, name='tax_reports'),
]
