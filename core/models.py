from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = (
        ('citizen', 'Citizen'),
        ('government', 'Government Official'),
        ('admin', 'Administrator'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='citizen')
    pan_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    
    # Add these to resolve the conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',  # Changed from default
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',  # Changed from default
        related_query_name='user',
    )
    
    def __str__(self):
        return f"{self.username} ({self.role})"


class SuccessStory(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='success_stories/')
    region = models.CharField(max_length=100)
    funds_used = models.DecimalField(max_digits=12, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
