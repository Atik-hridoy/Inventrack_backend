from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [
        'email',
        'password',
        'role',
        'is_approved',
        'is_active_staff',
    ]
    list_filter = ['role', 'is_approved', 'is_active_staff']

    def get_readonly_fields(self, request, obj=None):
        # Make checkboxes read-only for users, editable for staff/admin
        if obj and obj.role == 'user':
            return ['is_approved', 'is_active_staff']
        return []