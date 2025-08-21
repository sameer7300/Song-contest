from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number (optional)'}))
    city = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City (optional)'}))
    age = forms.IntegerField(
        required=False, 
        min_value=1, 
        max_value=120,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age (optional)'})
    )
    gender = forms.ChoiceField(
        choices=User.Gender.choices,
        initial=User.Gender.PREFER_NOT_TO_SAY,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'gender', 'phone_number', 'city', 'age', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }
        help_texts = {
            'username': 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].label = 'Gender (optional)'
        self.fields['gender'].choices = [('', 'Select gender (optional)')] + list(User.Gender.choices)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        user.city = self.cleaned_data['city']
        user.age = self.cleaned_data['age']
        user.gender = self.cleaned_data.get('gender', User.Gender.PREFER_NOT_TO_SAY)
        if commit:
            user.save()
        return user


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'autofocus': True
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No account found with this email address.")
        return email


class PasswordResetVerifyForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': '000000',
            'maxlength': '6',
            'style': 'letter-spacing: 0.5em; font-size: 1.5rem;'
        })
    )

    def clean_code(self):
        code = self.cleaned_data['code']
        if not code.isdigit() or len(code) != 6:
            raise forms.ValidationError("Please enter a valid 6-digit code.")
        return code


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New password'
        }),
        help_text="Your password must contain at least 8 characters."
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )


class UsernameRecoveryRequestForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'autofocus': True
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No account found with this email address.")
        return email


class UsernameRecoveryVerifyForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': '000000',
            'maxlength': '6',
            'style': 'letter-spacing: 0.5em; font-size: 1.5rem;'
        })
    )

    def clean_code(self):
        code = self.cleaned_data['code']
        if not code.isdigit() or len(code) != 6:
            raise forms.ValidationError("Please enter a valid 6-digit code.")
        return code
