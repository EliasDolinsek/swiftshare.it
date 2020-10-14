from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class NewPostForm(forms.Form):
    storage_duration = forms.ChoiceField(choices=Post.STORAGE_DURATIONS)
    keyword = forms.CharField(max_length=32, required=True)
    password = forms.CharField(max_length=32, required=False, widget=forms.PasswordInput(), label_suffix='(Optional)')
    confirm_password = forms.CharField(max_length=32, required=False, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(NewPostForm, self).clean()
        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise ValidationError('Passwords do not match')

        if Post.objects.filter(pk=cleaned_data['keyword']).exists():
            raise ValidationError('Keyword already exists')