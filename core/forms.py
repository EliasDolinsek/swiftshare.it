from django import forms
from django.core.exceptions import ValidationError
from .models import Post
import tinymce.widgets as tinymce_widgets


class NewPostForm(forms.Form):
    storage_duration = forms.ChoiceField(choices=Post.STORAGE_DURATIONS)
    keyword = forms.CharField(max_length=32, required=True)
    password = forms.CharField(max_length=32, required=True, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=32, required=True, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(NewPostForm, self).clean()
        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise ValidationError('Passwords do not match')

        if Post.objects.filter(pk=cleaned_data['keyword']).exists():
            raise ValidationError('Keyword already exists')


class PostContentForm(forms.Form):
    text = forms.CharField(required=False, widget=tinymce_widgets.TinyMCE())
    file = forms.FileField(required=False)