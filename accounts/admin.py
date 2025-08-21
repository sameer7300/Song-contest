from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_gender_display', 'phone_number', 'city', 'age', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'city', 'gender')
    search_fields = ('username', 'email', 'phone_number', 'first_name', 'last_name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('gender', 'phone_number', 'city', 'age', 'bio', 'avatar', 'website', 'social_media')}),
    )
    
    def get_gender_display(self, obj):
        return obj.get_gender_display()
    get_gender_display.short_description = 'Gender'
