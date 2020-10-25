from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', "email")


class PublicUserChangeForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PublicUserChangeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email")

    def save(self, commit=False):
        cleaned_data = self.cleaned_data
        self.user.first_name = cleaned_data["first_name"]
        self.user.last_name = cleaned_data["last_name"]

        if self.user.email != cleaned_data["email"]:
            self.user.email = cleaned_data["email"]

        self.user.save()

    def clean_email(self):
        email = self.cleaned_data["email"]
        if CustomUser.objects.filter(email=email).exists() and self.user.email != email:
            raise ValidationError("E-Mail already used by another account")
        else:
            return email
