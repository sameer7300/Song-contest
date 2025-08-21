from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import EmailVerification
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class EmailVerificationService:
    
    @staticmethod
    def send_notification_email(user, email, notification_type, context=None):
        """Send notification emails (song upload, winner announcement, etc.)"""
        try:
            if context is None:
                context = {}
            
            context.update({
                'user': user,
                'admin_email': settings.ADMIN_EMAIL
            })
            
            if notification_type == 'song_upload':
                subject = 'Song Upload Confirmation - AI Song Contest'
                template_html = 'email_verification/song_upload_notification.html'
                template_txt = 'email_verification/song_upload_notification.txt'
            elif notification_type == 'winner_announcement':
                subject = '🎉 Congratulations! You Won the AI Song Contest!'
                template_html = 'email_verification/winner_notification.html'
                template_txt = 'email_verification/winner_notification.txt'
            else:
                raise ValueError(f"Unknown notification type: {notification_type}")
            
            # Render email templates
            html_message = render_to_string(template_html, context)
            plain_message = render_to_string(template_txt, context)
            
            # Send email
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f"Notification email sent to {email} for {notification_type}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send notification email to {email}: {str(e)}")
            return False
    
    @staticmethod
    def send_verification_code(user, email, verification_type='registration'):
        """Send verification code to user's email"""
        try:
            # Create or update verification record
            verification, created = EmailVerification.objects.get_or_create(
                user=user,
                email=email,
                verification_type=verification_type,
                is_used=False,
                defaults={'attempts': 0}
            )
            
            if not created:
                # Reset existing verification
                verification.code = verification.generate_code()
                verification.attempts = 0
                verification.is_used = False
                verification.save()
            
            # Prepare email content based on verification type
            if verification_type == 'password_reset':
                subject = f'Password Reset Code - AI Song Contest'
                template_html = 'email_verification/password_reset_email.html'
                template_txt = 'email_verification/password_reset_email.txt'
            elif verification_type == 'username_recovery':
                subject = f'Username Recovery Code - AI Song Contest'
                template_html = 'email_verification/username_recovery_email.html'
                template_txt = 'email_verification/username_recovery_email.txt'
            else:
                subject = f'Your verification code for AI Song Contest'
                template_html = 'email_verification/verification_code_email.html'
                template_txt = 'email_verification/verification_code_email.txt'
            
            context = {
                'user': user,
                'code': verification.code,
                'verification_type': verification_type,
                'expires_minutes': 15
            }
            
            # Render email templates
            html_message = render_to_string(template_html, context)
            plain_message = render_to_string(template_txt, context)
            
            # Send email
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f"Verification code sent to {email} for {verification_type}")
            return verification
            
        except Exception as e:
            logger.error(f"Failed to send verification code to {email}: {str(e)}")
            raise e
    
    @staticmethod
    def verify_code(user, email, code, verification_type='registration'):
        """Verify the provided code"""
        try:
            verification = EmailVerification.objects.get(
                user=user,
                email=email,
                verification_type=verification_type,
                code=code,
                is_used=False
            )
            
            # Increment attempts
            verification.attempts += 1
            verification.save()
            
            if not verification.is_valid():
                if verification.is_expired():
                    return False, "Verification code has expired. Please request a new one."
                elif verification.attempts >= 5:
                    return False, "Too many failed attempts. Please request a new code."
                else:
                    return False, "Invalid verification code."
            
            # Mark as used
            verification.is_used = True
            verification.save()
            
            logger.info(f"Verification successful for {email}")
            return True, "Email verified successfully!"
            
        except EmailVerification.DoesNotExist:
            return False, "Invalid verification code."
        except Exception as e:
            logger.error(f"Error verifying code for {email}: {str(e)}")
            return False, "An error occurred during verification."
    
    @staticmethod
    def cleanup_expired_codes():
        """Clean up expired verification codes"""
        from django.utils import timezone
        expired_count = EmailVerification.objects.filter(
            expires_at__lt=timezone.now()
        ).delete()[0]
        logger.info(f"Cleaned up {expired_count} expired verification codes")
        return expired_count
