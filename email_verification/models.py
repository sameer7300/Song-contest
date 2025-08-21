from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import random
import string
from datetime import timedelta

User = get_user_model()

class EmailVerification(models.Model):
    VERIFICATION_TYPES = [
        ('registration', 'Registration'),
        ('login', 'Login'),
        ('password_reset', 'Password Reset'),
        ('username_recovery', 'Username Recovery'),
        ('song_deletion', 'Song Deletion'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verifications')
    email = models.EmailField()
    code = models.CharField(max_length=6)
    verification_type = models.CharField(max_length=20, choices=VERIFICATION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=15)  # 15 minutes expiry
        super().save(*args, **kwargs)
    
    def generate_code(self):
        """Generate a 6-digit verification code"""
        return ''.join(random.choices(string.digits, k=6))
    
    def is_expired(self):
        """Check if the verification code has expired"""
        return timezone.now() > self.expires_at
    
    def is_valid(self):
        """Check if the verification code is valid (not used, not expired, attempts < 5)"""
        return not self.is_used and not self.is_expired() and self.attempts < 5
    
    def __str__(self):
        return f"{self.email} - {self.verification_type} - {self.code}"
