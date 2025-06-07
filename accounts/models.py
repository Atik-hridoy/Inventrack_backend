from django.db import models

class Account(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('user', 'User'),
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, default='defaultuser')

    password = models.CharField(max_length=128)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_approved = models.BooleanField(default=False)
    is_active_staff = models.BooleanField(default=True)
    raw_password = models.CharField(max_length=128, blank=True, null=True)  # For testing only!

    def __str__(self):
        return self.email