from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_password_reset_email(user):
    subject = "Password Reset Requested"
    email_template_name = "accounts/password_reset/password_reset_email.txt"
    c = {
        "email": user.email,
        'domain': '127.0.0.1:8000',
        'site_name': 'Website',
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "user": user,
        'token': default_token_generator.make_token(user),
        'protocol': 'http',
    }
    email = render_to_string(email_template_name, c)
    try:
        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return redirect("accounts:password_reset_done")
