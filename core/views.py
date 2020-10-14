from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings

from . import forms

# Create your views here.
from .models import Post


def index(request):
    return render(request, 'core/index.html')


def new_post(request):
    if request.method == 'POST':
        form = forms.NewPostForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            post = Post(
                storage_duration=cleaned_data['storage_duration'],
                keyword=cleaned_data['keyword'],
                password=cleaned_data['password']
            )

            post.save()
            return HttpResponseRedirect(reverse('core:edit_post', kwargs={'pk': post.pk}))
    else:
        form = forms.NewPostForm()

    return render(request, 'core/new_post.html', {'form': form})


def edit_post(request, pk):
    if request.method == 'POST':
        form = forms.PostContentForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            post = get_object_or_404(Post, pk=pk)

            post.text = cleaned_data['text']

            file = request.FILES.get('file', None)
            post.file = file
            if file is not None:
                post.upload_file(file)

            post.save()
            return redirect('core:show_post', pk=pk)
    else:
        form = forms.PostContentForm()

    return render(request, 'core/edit_post.html', {'form': form})


def show_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'core/details.html', {'post': post})


def open_post(request):
    form = forms.OpenPostForm(request.POST or None)
    if form.is_valid():
        keyword = form.cleaned_data['keyword']
        return redirect('core:show_post', pk=keyword)
    else:
        return render(request, 'core/open_post.html', {'form': form})
