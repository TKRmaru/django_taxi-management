from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                (" アカウントが無効です "),
                code='inactive',
            )
