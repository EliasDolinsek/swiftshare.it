from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render, redirect, get_object_or_404

from core.models import Namespace
from .forms import CustomUserCreationForm, PublicUserChangeForm, DeleteAccountForm, CreateNamespaceForm, \
    UpdateNamespaceForm, CustomAuthenticationForm
from .email_helper import send_password_reset_email
# Create your views here.
from .models import CustomUser


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:home")
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/auth/register.html', context={'form': form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect("accounts:home")
    if request.method == "POST":
        form = CustomAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(email=cleaned_data["username"], password=cleaned_data["password"])
            if user is not None:
                login(request, user=user)
                return redirect("accounts:home")
    else:
        form = CustomAuthenticationForm()

    return render(request, "accounts/auth/login.html", context={"form": form})


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
    return render(request, 'accounts/account_details/namespaces/namespaces.html', context)


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


@login_required
def namespace_details(request, name):
    try:
        namespace = Namespace.objects.get(name__exact=name)
    except Namespace.DoesNotExist:
        return redirect("accounts:namespaces")

    if request.method == "POST":
        form = UpdateNamespaceForm(namespace, request.POST)
        if form.is_valid():
            new_namespace_name = form.cleaned_data["name"]
            namespace.name = new_namespace_name
            namespace.save()
            return redirect("accounts:namespace_details", name=new_namespace_name, permanent=True)
    else:
        form = UpdateNamespaceForm(namespace)

    context = {
        "form": form,
        "namespace": namespace,
        "namespace_posts": namespace.post_set.all()
    }
    return render(request, 'accounts/account_details/namespaces/namespace_details.html', context)


@login_required
def delete_namespace(request, name):
    namespace = get_object_or_404(Namespace, name=name)
    if request.method == "POST":
        namespace.delete()
        return redirect("accounts:delete_namespace_success")
    else:
        return render(request, "accounts/account_details/namespaces/delete_namespace.html", {"namespace": namespace})


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = CustomUser.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    send_password_reset_email(user)
            return redirect("accounts:password_reset_done")
    else:
        password_reset_form = PasswordResetForm()
    return render(request, "accounts/password_reset/password_reset.html", {"password_reset_form": password_reset_form})
