from django.http import HttpResponse
from django.shortcuts import render
from .forms import CustomUserCreationForm, CustomUserChangeForm


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("User created successfully")
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', context={'form': form})
