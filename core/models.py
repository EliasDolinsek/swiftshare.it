import os

from django.db import models

# Create your models here.
from tinymce.models import HTMLField
from django.conf import settings


class Post(models.Model):
    STORAGE_DURATIONS = (
        (0, '6h'),
        (1, '1d'),
        (1, '7d')
    )

    keyword = models.CharField(primary_key=True, max_length=32, blank=False, null=False, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    storage_duration = models.IntegerField(choices=STORAGE_DURATIONS, default=0)
    password = models.CharField(max_length=32, blank=True, null=False)

    text = HTMLField()
    file = models.FileField(upload_to=f'files/{keyword}/', blank=True)

    def password_enabled(self):
        return not self.password

    def upload_file(self, file):
        file_path = os.path.join(settings.MEDIA_ROOT, f'files/{self.keyword}/{file.name}')

        if not os.path.exists(os.path.dirname(file_path)):
            try:
                os.makedirs(os.path.dirname(file_path))
            except OSError as exc:
                raise OSError(f"Couldn't create path for file {file_path}")

        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
