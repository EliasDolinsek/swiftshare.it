import datetime
import os

from django.db import models

# Create your models here.

from tinymce.models import HTMLField
from django.conf import settings

from accounts.models import CustomUser


class Post(models.Model):
    STORAGE_DURATIONS = (
        (0, '6h'),
        (1, '1d'),
        (2, '7d')
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    keyword = models.CharField(primary_key=True, max_length=32, blank=False, null=False, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    storage_duration = models.IntegerField(choices=STORAGE_DURATIONS, default=0)
    password = models.CharField(max_length=32, blank=True, null=False)

    text = models.TextField(max_length=100000, blank=True, default="")
    file = models.FileField(upload_to=f'files/{keyword}/', blank=True)

    def removal_date(self):
        return self.creation_date + self.get_timedelta_for_storage_duration()

    def get_timedelta_for_storage_duration(self):
        return (
            datetime.timedelta(hours=6),
            datetime.timedelta(days=1),
            datetime.timedelta(days=7)
        )[self.storage_duration]

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

    def __str__(self):
        return self.keyword

    def get_filename(self):
        return os.path.basename(self.file.name)

    def get_file_size(self):
        value = self.file.size
        if value < 512000:
            value = value / 1024.0
            ext = 'kb'
        elif value < 4194304000:
            value = value / 1048576.0
            ext = 'mb'
        else:
            value = value / 1073741824.0
            ext = 'gb'
        return '%s %s' % (str(round(value, 2)), ext)

    def get_link(self):
        return f"swsh.it/{self.keyword}"
