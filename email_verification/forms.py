from django import forms
from django.contrib.auth import get_user_model
from .models import EmailVerification

User = get_user_model()

class EmailVerificationForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': '000000',
            'style': 'font-size: 1.5rem; letter-spacing: 0.5rem;',
            'maxlength': '6',
            'pattern': '[0-9]{6}',
            'title': 'Please enter a 6-digit code'
        }),
        help_text='Enter the 6-digit code sent to your email'
    )
    
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not code.isdigit():
            raise forms.ValidationError('Code must contain only numbers.')
        return code

class ResendCodeForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
