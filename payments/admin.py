from django.contrib import admin
from .models import Transaction
from accounts.models import UserRole
from django.utils import timezone
from datetime import timedelta

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['reference', 'amount', 'status', 'initiated_by', 'customer', 'created_at']
    list_filter = ['status', 'payment_method', 'initiated_by__role']
    search_fields = ['reference', 'phone_number']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == UserRole.OPERATOR:
            return qs.filter(created_at__gte=timezone.now() - timedelta(days=30))
        return qs
        
    def has_delete_permission(self, request, obj=None):
        return request.user.role == UserRole.ADMIN
    
admin.site.register(Transaction, TransactionAdmin)