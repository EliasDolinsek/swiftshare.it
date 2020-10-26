from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, PublicUserChangeForm, DeleteAccountForm, CreateNamespaceForm

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
    if request.method == "POST":
        form = CreateNamespaceForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            form = CreateNamespaceForm(request.user)
    else:
        form = CreateNamespaceForm(request.user)

    user_namespaces = request.user.namespace_set.all()
    context = {
        "form": form,
        "namespaces": user_namespaces
    }
    return render(request, 'accounts/account_details/namespaces.html', context)


@login_required
def settings(request, **kwargs):
    print(kwargs)
    user = request.user

    success_message = ""
    if request.method == 'POST':
        form = PublicUserChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            success_message = "Updated details successfully"
    else:
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }
        form = PublicUserChangeForm(user, initial=initial_data)

    context = {
        "form": form,
        "success_message": success_message
    }

    return render(request, 'accounts/account_details/settings/settings.html', context)


@login_required
def change_password_success(request):
    return render(request, 'accounts/account_details/settings/change_password/change_password_success.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect("core:index")


@login_required
def delete_account(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.user, request.POST)
        if form.is_valid():
            request.user.delete()
            return redirect('accounts:delete_account_success')
    else:
        form = DeleteAccountForm(request.user)

    return render(request, 'accounts/account_details/settings/delete_account/delete_account.html', {"form": form})


def delete_account_success(request):
    return render(request, 'accounts/account_details/settings/delete_account/delete_account_success.html')
