from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('fund-tracker/', views.fund_tracker, name='fund_tracker'),
    path('success-stories/', views.success_stories, name='success_stories'),
    path('logout/', views.custom_logout, name='logout'),
]
