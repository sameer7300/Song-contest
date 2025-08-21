from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')
        PREFER_NOT_TO_SAY = 'N', _('Prefer not to say')
    
    phone_number = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        default=Gender.PREFER_NOT_TO_SAY,
        verbose_name=_('gender')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Profile enhancements
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    website = models.URLField(blank=True)
    social_media = models.CharField(max_length=100, blank=True, help_text="Instagram/Twitter handle")
    is_verified = models.BooleanField(default=False)
    
    # Statistics
    total_votes_received = models.PositiveIntegerField(default=0)
    total_songs_uploaded = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.username
    
    def get_display_name(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.username
