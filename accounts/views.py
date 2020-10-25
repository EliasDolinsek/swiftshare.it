from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, PublicUserChangeForm


# Create your views here.
from .models import CustomUser


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("User created successfully")
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', context={'form': form})


@login_required
def home(request):
    return redirect('accounts:posts')


@login_required
def posts(request):
    current_user = request.user
    user_posts = current_user.post_set.all()
    return render(request, 'accounts/account_details/posts.html', {'user_posts': user_posts})


@login_required
def namespaces(request):
    return render(request, 'accounts/account_details/namespaces.html')


@login_required
def settings(request):
    user = request.user
    if request.method == 'POST':
        form = PublicUserChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
    else:
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }
        form = PublicUserChangeForm(user, initial=initial_data)
    return render(request, 'accounts/account_details/settings.html', {'form': form})
