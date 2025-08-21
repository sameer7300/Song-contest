from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Winner, Song
from email_verification.services import EmailVerificationService
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Winner)
def send_winner_notification(sender, instance, created, **kwargs):
    """Send email notification when a user is announced as winner"""
    if created:  # Only send email when winner is first created
        try:
            song = instance.song
            user = song.user
            
            # Send winner notification email
            EmailVerificationService.send_notification_email(
                user,
                user.email,
                'winner_announcement',
                {
                    'song': song,
                    'winner': instance
                }
            )
            
            logger.info(f"Winner notification sent to {user.email} for song: {song.title}")
            
        except Exception as e:
            logger.error(f"Failed to send winner notification: {str(e)}")

@receiver(post_save, sender=Song)
def update_song_winner_status(sender, instance, **kwargs):
    """Update song's is_winner status when Winner object is created/deleted"""
    try:
        # Check if this song has a Winner record
        has_winner = Winner.objects.filter(song=instance).exists()
        
        # Update song's is_winner field if it doesn't match
        if instance.is_winner != has_winner:
            instance.is_winner = has_winner
            instance.save(update_fields=['is_winner'])
            
    except Exception as e:
        logger.error(f"Error updating song winner status: {str(e)}")
