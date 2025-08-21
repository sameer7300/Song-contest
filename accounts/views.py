from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import (
    SignUpForm, PasswordResetRequestForm, PasswordResetVerifyForm, CustomSetPasswordForm,
    UsernameRecoveryRequestForm, UsernameRecoveryVerifyForm
)
from email_verification.services import EmailVerificationService

User = get_user_model()

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        user = form.get_user()
        
        # Check if user needs email verification
        if not user.is_active:
            # Send verification code
            try:
                EmailVerificationService.send_verification_code(
                    user, user.email, 'login'
                )
                
                # Set session data for verification
                self.request.session['pending_verification'] = True
                self.request.session['pending_verification_user_id'] = user.id
                self.request.session['pending_verification_email'] = user.email
                self.request.session['verification_type'] = 'login'
                
                messages.info(self.request, 'Please verify your email to complete login.')
                return redirect('email_verification:verify_email')
                
            except Exception as e:
                messages.error(self.request, 'Failed to send verification code. Please try again.')
                return self.form_invalid(form)
        
        # Normal login flow
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('contest:home')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Require email verification
            user.save()
            
            try:
                # Send verification code
                EmailVerificationService.send_verification_code(
                    user, user.email, 'registration'
                )
                
                # Set session data for verification
                request.session['pending_verification'] = True
                request.session['pending_verification_user_id'] = user.id
                request.session['pending_verification_email'] = user.email
                request.session['verification_type'] = 'registration'
                
                messages.success(request, 'Registration successful! Please check your email for a verification code.')
                return redirect('email_verification:verify_email')
                
            except Exception as e:
                # If email fails, delete the user and show error
                user.delete()
                messages.error(request, 'Failed to send verification email. Please try again.')
                
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def password_reset_request_view(request):
    """Request password reset by email"""
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            
            try:
                # Send verification code for password reset
                EmailVerificationService.send_verification_code(
                    user, email, 'password_reset'
                )
                
                # Set session data for verification
                request.session['pending_password_reset'] = True
                request.session['password_reset_user_id'] = user.id
                request.session['password_reset_email'] = email
                
                messages.success(request, 'Password reset code sent to your email.')
                return redirect('accounts:password_reset_verify')
                
            except Exception as e:
                messages.error(request, 'Failed to send reset code. Please try again.')
                
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'accounts/password_reset_request.html', {'form': form})


def password_reset_verify_view(request):
    """Verify password reset code"""
    if not request.session.get('pending_password_reset'):
        messages.error(request, 'No password reset request found.')
        return redirect('accounts:password_reset_request')
    
    user_id = request.session.get('password_reset_user_id')
    email = request.session.get('password_reset_email')
    user = get_object_or_404(User, id=user_id, email=email)
    
    if request.method == 'POST':
        form = PasswordResetVerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            
            # Verify the code
            success, message = EmailVerificationService.verify_code(
                user, email, code, 'password_reset'
            )
            
            if success:
                # Set session for password reset
                request.session['password_reset_verified'] = True
                messages.success(request, 'Code verified! Please set your new password.')
                return redirect('accounts:password_reset_confirm')
            else:
                messages.error(request, message)
    else:
        form = PasswordResetVerifyForm()
    
    context = {
        'form': form,
        'email': email
    }
    return render(request, 'accounts/password_reset_verify.html', context)


def password_reset_confirm_view(request):
    """Set new password after verification"""
    if not request.session.get('password_reset_verified'):
        messages.error(request, 'Please verify your email first.')
        return redirect('accounts:password_reset_request')
    
    user_id = request.session.get('password_reset_user_id')
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = CustomSetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            
            # Clear session data
            request.session.pop('pending_password_reset', None)
            request.session.pop('password_reset_user_id', None)
            request.session.pop('password_reset_email', None)
            request.session.pop('password_reset_verified', None)
            
            messages.success(request, 'Password reset successfully! You can now login with your new password.')
            return redirect('accounts:login')
    else:
        form = CustomSetPasswordForm(user)
    
    return render(request, 'accounts/password_reset_confirm.html', {'form': form})


def username_recovery_request_view(request):
    """Request username recovery by email"""
    if request.method == 'POST':
        form = UsernameRecoveryRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            
            try:
                # Send verification code for username recovery
                EmailVerificationService.send_verification_code(
                    user, email, 'username_recovery'
                )
                
                # Set session data for verification
                request.session['pending_username_recovery'] = True
                request.session['username_recovery_user_id'] = user.id
                request.session['username_recovery_email'] = email
                
                messages.success(request, 'Username recovery code sent to your email.')
                return redirect('accounts:username_recovery_verify')
                
            except Exception as e:
                messages.error(request, 'Failed to send recovery code. Please try again.')
                
    else:
        form = UsernameRecoveryRequestForm()
    
    return render(request, 'accounts/username_recovery_request.html', {'form': form})


def username_recovery_verify_view(request):
    """Verify username recovery code and show username"""
    if not request.session.get('pending_username_recovery'):
        messages.error(request, 'No username recovery request found.')
        return redirect('accounts:username_recovery_request')
    
    user_id = request.session.get('username_recovery_user_id')
    email = request.session.get('username_recovery_email')
    user = get_object_or_404(User, id=user_id, email=email)
    
    if request.method == 'POST':
        form = UsernameRecoveryVerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            
            # Verify the code
            success, message = EmailVerificationService.verify_code(
                user, email, code, 'username_recovery'
            )
            
            if success:
                # Clear session data
                request.session.pop('pending_username_recovery', None)
                request.session.pop('username_recovery_user_id', None)
                request.session.pop('username_recovery_email', None)
                
                # Show username
                messages.success(request, f'Your username is: {user.username}')
                return render(request, 'accounts/username_recovery_success.html', {'username': user.username})
            else:
                messages.error(request, message)
    else:
        form = UsernameRecoveryVerifyForm()
    
    context = {
        'form': form,
        'email': email
    }
    return render(request, 'accounts/username_recovery_verify.html', context)
