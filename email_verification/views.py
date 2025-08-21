from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import EmailVerification
from .forms import EmailVerificationForm, ResendCodeForm
from .services import EmailVerificationService
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

def verify_email(request):
    """Email verification view"""
    if not request.session.get('pending_verification'):
        messages.error(request, 'No pending verification found.')
        return redirect('accounts:login')
    
    user_id = request.session.get('pending_verification_user_id')
    email = request.session.get('pending_verification_email')
    verification_type = request.session.get('verification_type', 'registration')
    
    if not user_id or not email:
        messages.error(request, 'Invalid verification session.')
        return redirect('accounts:login')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            success, message = EmailVerificationService.verify_code(
                user, email, code, verification_type
            )
            
            if success:
                # Clear session data
                request.session.pop('pending_verification', None)
                request.session.pop('pending_verification_user_id', None)
                request.session.pop('pending_verification_email', None)
                request.session.pop('verification_type', None)
                
                # Mark user as verified if registration
                if verification_type == 'registration':
                    user.is_active = True
                    user.save()
                
                messages.success(request, message)
                return redirect('contest:dashboard')
            else:
                messages.error(request, message)
    else:
        form = EmailVerificationForm()
    
    # Check for existing verification
    try:
        verification = EmailVerification.objects.get(
            user=user,
            email=email,
            verification_type=verification_type,
            is_used=False
        )
        time_remaining = max(0, int((verification.expires_at - timezone.now()).total_seconds() / 60))
    except EmailVerification.DoesNotExist:
        time_remaining = 0
    
    context = {
        'form': form,
        'email': email,
        'verification_type': verification_type,
        'time_remaining': time_remaining,
        'user': user
    }
    
    return render(request, 'email_verification/verify_email.html', context)

@require_POST
def resend_verification_code(request):
    """Resend verification code"""
    if not request.session.get('pending_verification'):
        return JsonResponse({'success': False, 'message': 'No pending verification found.'})
    
    user_id = request.session.get('pending_verification_user_id')
    email = request.session.get('pending_verification_email')
    verification_type = request.session.get('verification_type', 'registration')
    
    if not user_id or not email:
        return JsonResponse({'success': False, 'message': 'Invalid verification session.'})
    
    try:
        user = get_object_or_404(User, id=user_id)
        
        # Check rate limiting (max 3 codes per 10 minutes)
        recent_codes = EmailVerification.objects.filter(
            user=user,
            email=email,
            verification_type=verification_type,
            created_at__gte=timezone.now() - timezone.timedelta(minutes=10)
        ).count()
        
        if recent_codes >= 3:
            return JsonResponse({
                'success': False, 
                'message': 'Too many requests. Please wait 10 minutes before requesting a new code.'
            })
        
        # Send new verification code
        verification = EmailVerificationService.send_verification_code(
            user, email, verification_type
        )
        
        return JsonResponse({
            'success': True, 
            'message': 'A new verification code has been sent to your email.',
            'expires_at': verification.expires_at.isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error resending verification code: {str(e)}")
        return JsonResponse({
            'success': False, 
            'message': 'Failed to send verification code. Please try again later.'
        })
