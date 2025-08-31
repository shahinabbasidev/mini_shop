from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from account.models import User


class UserCreationForm(forms.ModelForm):
    """Form for creating new users with password confirmation."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["phone", "full_name", "email"]

    def clean_password2(self):
        """Check that the two password entries match."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """Save the provided password in hashed format."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """Form for updating users. Shows the hashed password field read-only."""

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["phone", "full_name", "email", "password", "is_active", "is_admin", "is_staff", "is_superuser"]


class LoginForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone number"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )
