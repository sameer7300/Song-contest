from django.urls import path
from .views import (
    signup_view, CustomLoginView, CustomLogoutView,
    password_reset_request_view, password_reset_verify_view, password_reset_confirm_view,
    username_recovery_request_view, username_recovery_verify_view
)

app_name = 'accounts'

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('password-reset/', password_reset_request_view, name='password_reset_request'),
    path('password-reset/verify/', password_reset_verify_view, name='password_reset_verify'),
    path('password-reset/confirm/', password_reset_confirm_view, name='password_reset_confirm'),
    path('username-recovery/', username_recovery_request_view, name='username_recovery_request'),
    path('username-recovery/verify/', username_recovery_verify_view, name='username_recovery_verify'),
]