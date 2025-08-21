from django.contrib import admin
from .models import EmailVerification

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['email', 'verification_type', 'code', 'created_at', 'expires_at', 'is_used', 'attempts']
    list_filter = ['verification_type', 'is_used', 'created_at']
    search_fields = ['email', 'code']
    readonly_fields = ['code', 'created_at', 'expires_at']
    ordering = ['-created_at']
