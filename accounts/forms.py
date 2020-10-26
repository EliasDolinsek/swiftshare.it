from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django import forms

from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', "email")


class PublicUserChangeForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PublicUserChangeForm, self).__init__(*args, **kwargs)

    def save(self):
        cleaned_data = self.cleaned_data
        cleaned_first_name = cleaned_data["first_name"]
        cleaned_last_name = cleaned_data["last_name"]
        cleaned_email = cleaned_data["email"]

        if cleaned_first_name:
            self.user.first_name = cleaned_data["first_name"]

        if cleaned_last_name:
            self.user.last_name = cleaned_data["last_name"]

        if cleaned_email:
            self.user.email = cleaned_email

        self.user.save()

    def clean_email(self):
        email = self.cleaned_data["email"]
        if CustomUser.objects.filter(email=email).exists() and self.user.email != email:
            raise ValidationError("E-Mail already used by another account")
        else:
            return email


class DeleteAccountForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(DeleteAccountForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        cleaned_password = self.cleaned_data["password"]
        if self.user.check_password(cleaned_password):
            return cleaned_password
        else:
            raise ValidationError("Invalid password")
