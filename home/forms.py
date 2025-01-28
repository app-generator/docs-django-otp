from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class OtpEmailForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email address'
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError("No user is associated with this email address.")
        return email
