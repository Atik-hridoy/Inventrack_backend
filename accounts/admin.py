from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [
        'email',
        'username',
        'role',
        'is_approved',
        'is_active_staff',
    ]
    list_filter = ['role', 'is_approved', 'is_active_staff']
    search_fields = ['email', 'username']
    ordering = ['email']

    def get_readonly_fields(self, request, obj=None):
        # Make some fields read-only if editing an existing user
        if obj and obj.role == 'user':
            return ['is_approved', 'is_active_staff']
        return []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=False)
