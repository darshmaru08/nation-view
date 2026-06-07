from django.urls import path
from . import views

urlpatterns = [
    path('submit-tax/', views.submit_tax, name='submit_tax'),
    path('my-taxes/', views.my_taxes, name='my_taxes'),
    path('feedback/', views.feedback, name='feedback'),
]
