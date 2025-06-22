from django.contrib import admin
from .models import Account, UserProfileEditHistory

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [
        'email',
        'username',
        'role',
        'is_approved',
        'is_active_staff',
        'phone',
        'nickname',
        'address_street',
        'address_house',
        'address_district',
    ]
    list_filter = ['role', 'is_approved', 'is_active_staff']
    search_fields = ['email', 'username', 'phone', 'nickname', 'address_street', 'address_house', 'address_district']
    ordering = ['email']

    def get_readonly_fields(self, request, obj=None):
        # Make some fields read-only if editing an existing user
        if obj and obj.role == 'user':
            return ['is_approved', 'is_active_staff']
        return []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=False)

@admin.register(UserProfileEditHistory)
class UserProfileEditHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'field_changed', 'old_value', 'new_value', 'edited_at']
    search_fields = ['user__email', 'field_changed', 'old_value', 'new_value']
    list_filter = ['field_changed', 'edited_at']
