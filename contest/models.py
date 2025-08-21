from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.db.models import Avg, Count

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    color = models.CharField(max_length=7, default='#007bff', help_text="Hex color code")
    
    def __str__(self):
        return self.name

class Song(models.Model):
    LANGUAGE_CHOICES = [
        ('urdu', 'Urdu'),
        ('english', 'English'),
    ]
    
    GENRE_CHOICES = [
        ('pop', 'Pop'),
        ('rock', 'Rock'),
        ('classical', 'Classical'),
        ('folk', 'Folk'),
        ('electronic', 'Electronic'),
        ('hip_hop', 'Hip Hop'),
        ('jazz', 'Jazz'),
        ('country', 'Country'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songs')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='other')
    ai_tool_used = models.CharField(max_length=100, help_text="e.g., Suno AI, Boomy, Soundraw, AIVA")
    tags = models.ManyToManyField(Tag, blank=True)
    
    # File uploads
    audio_file = models.FileField(
        upload_to='songs/audio/',
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav'])],
        help_text="Upload your song file (.mp3 or .wav, max 50MB)"
    )
    lyrics_file = models.FileField(
        upload_to='songs/lyrics/',
        validators=[FileExtensionValidator(allowed_extensions=['txt', 'pdf', 'doc', 'docx'])],
        help_text="Upload your lyrics file"
    )
    
    # Metadata
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    file_size_mb = models.FloatField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_winner = models.BooleanField(default=False)
    
    # Engagement metrics
    view_count = models.PositiveIntegerField(default=0)
    vote_count = models.PositiveIntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    
    # Featured status
    is_featured = models.BooleanField(default=False)
    featured_until = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.title} by {self.user.username}"
    
    def get_rating_display(self):
        return f"{self.average_rating:.1f}" if self.average_rating > 0 else "No ratings"
    
    def update_rating(self):
        """Update average rating based on votes"""
        votes = self.votes.all()
        if votes.exists():
            self.average_rating = votes.aggregate(avg=Avg('rating'))['avg'] or 0
            self.vote_count = votes.count()
        else:
            self.average_rating = 0
            self.vote_count = 0
        self.save()
    
    def increment_view_count(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])

class Vote(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='votes')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'song')  # One vote per user per song
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} rated {self.song.title}: {self.rating} stars"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.song.title}"

class Winner(models.Model):
    song = models.OneToOneField(Song, on_delete=models.CASCADE, related_name='winner_info')
    selected_at = models.DateTimeField(auto_now_add=True)
    admin_notes = models.TextField(blank=True)
    featured_until = models.DateTimeField(null=True, blank=True, help_text="When this winner expires from front page")
    prize_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        ordering = ['-selected_at']
    
    def __str__(self):
        return f"Winner: {self.song.title}"


class Deadline(models.Model):
    STATUS_CHOICES = [
        ('open_for_submission', 'Open for Song Submission'),
        ('judging', 'Judging Phase'),
        ('winner_announced', 'Winner Announced'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open_for_submission')
    description = models.TextField(blank=True, help_text="Optional description for this contest phase")
    deadline_date = models.DateTimeField(help_text="When this phase ends", default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_status_display()} - {self.deadline_date.strftime('%Y-%m-%d')}"

    @property
    def is_active(self):
        """Check if this deadline phase is currently active (not expired)"""
        from django.utils import timezone
        return timezone.now() <= self.deadline_date
    
    @property
    def time_remaining(self):
        """Get time remaining until deadline"""
        from django.utils import timezone
        if self.is_active:
            return self.deadline_date - timezone.now()
        return None
    
    @classmethod
    def get_current_phase(cls):
        """Get the current active contest phase"""
        from django.utils import timezone
        return cls.objects.filter(deadline_date__gte=timezone.now()).order_by('deadline_date').first()
    
    @classmethod
    def can_submit_songs(cls):
        """Check if songs can currently be submitted"""
        current_phase = cls.get_current_phase()
        return current_phase and current_phase.status == 'open_for_submission'
    
    @classmethod
    def check_and_advance_phases(cls):
        """Check for expired phases and automatically advance to next phase"""
        from django.utils import timezone
        now = timezone.now()
        
        # Get all expired phases that haven't been updated
        expired_phases = cls.objects.filter(deadline_date__lt=now).order_by('deadline_date')
        
        for phase in expired_phases:
            if phase.status == 'open_for_submission':
                # Advance to judging phase
                phase.status = 'judging'
                # Set judging deadline to 7 days from now (configurable)
                phase.deadline_date = now + timezone.timedelta(days=7)
                phase.description = "Contest submissions are now being evaluated by our judges."
                phase.save()
            elif phase.status == 'judging':
                # Advance to winner announced phase
                phase.status = 'winner_announced'
                # Set winner announcement to be active for 30 days (configurable)
                phase.deadline_date = now + timezone.timedelta(days=30)
                phase.description = "Winners have been announced! Check the winners page."
                phase.save()
            # winner_announced phase doesn't auto-advance (contest ends)
    
    @classmethod
    def get_phase_message(cls):
        """Get appropriate message for current phase"""
        current_phase = cls.get_current_phase()
        if not current_phase:
            return "No active contest phase found."
        
        if current_phase.status == 'open_for_submission':
            if current_phase.is_active:
                return f"Song submissions are open until {current_phase.deadline_date.strftime('%B %d, %Y at %I:%M %p')}."
            else:
                return "The submission deadline has passed. Submissions are now closed."
        elif current_phase.status == 'judging':
            if current_phase.is_active:
                return f"Contest is in judging phase. Results will be announced by {current_phase.deadline_date.strftime('%B %d, %Y')}."
            else:
                return "Judging phase has ended. Winners should be announced soon."
        elif current_phase.status == 'winner_announced':
            return "Winners have been announced! Check the winners page to see the results."
        
        return "Contest status unknown."
