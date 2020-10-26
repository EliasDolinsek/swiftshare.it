from django.contrib import admin
from .models import Post, Namespace

# Register your models here.
admin.site.register(Post)
admin.site.register(Namespace)