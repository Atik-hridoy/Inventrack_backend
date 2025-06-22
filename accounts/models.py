from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_approved', True)
        extra_fields.setdefault('is_active_staff', True)
        # Do NOT set role for superuser
        return self.create_user(email, username, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('staff', 'Staff'),
        ('user', 'User'),
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # AbstractBaseUser handles hashing

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_approved = models.BooleanField(default=False)
    is_active_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # New profile fields
    phone = models.CharField(max_length=20, blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    address_street = models.CharField(max_length=255, blank=True, null=True)
    address_house = models.CharField(max_length=50, blank=True, null=True)
    address_district = models.CharField(max_length=100, blank=True, null=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class UserProfileEditHistory(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='edit_histories')
    edited_at = models.DateTimeField(auto_now_add=True)
    field_changed = models.CharField(max_length=50)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} changed {self.field_changed} at {self.edited_at}"



