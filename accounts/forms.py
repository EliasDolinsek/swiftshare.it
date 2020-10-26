from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django import forms

from accounts.models import CustomUser
from core.models import Namespace


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')


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


class CreateNamespaceForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CreateNamespaceForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Namespace
        fields = ("name",)

    def save(self, commit=True):
        model = super(CreateNamespaceForm, self).save(commit=False)
        model.user = self.user
        if commit:
            model.save()


class UpdateNamespaceForm(forms.Form):
    name = forms.CharField(max_length=32)

    def __init__(self, namespace, *args, **kwargs):
        self.namespace = namespace
        super(UpdateNamespaceForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        cleaned_name = self.cleaned_data["name"]
        filtered_namespaces = Namespace.objects.filter(name__exact=cleaned_name)
        if filtered_namespaces.exists() and filtered_namespaces[0] != self.namespace:
            raise ValidationError("Namespace with this Name already exists")
        return cleaned_name
