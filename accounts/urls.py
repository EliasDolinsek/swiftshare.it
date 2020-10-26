from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from accounts import views

app_name = "accounts"

urlpatterns = [
    path('', views.home, name="home"),
    path('posts/', views.posts, name="posts"),
    path('namespaces/', views.namespaces, name="namespaces"),
    path('namespaces/<str:name>', views.namespace_details, name="namespace_details"),
    path('namespaces/delete/<str:name>', views.delete_namespace, name="delete_namespace"),
    path('namespaces/delete-success/',
         TemplateView.as_view(template_name="accounts/account_details/namespaces/delete_namespace_success.html"),
         name="delete_namespace_success"),
    path('settings/', views.settings, name="settings"),
    path('settings/change-password/',
         auth_views.PasswordChangeView.as_view(
             template_name="accounts/account_details/settings/change_password/change_password.html",
             success_url=reverse_lazy('accounts:change_password_success')
         ),
         name="change_password"),
    path('settings/change-password/success/', TemplateView.as_view(
        template_name="accounts/account_details/settings/change_password/change_password_success.html"),
         name="change_password_success"),
    path('settings/logout/', views.logout_user, name="logout_user"),
    path('settings/delete-account/', views.delete_account, name="delete_account"),
    path('settings/delete-account/success/', TemplateView.as_view(
        template_name="accounts/account_details/settings/delete_account/delete_account_success.html"),
         name="delete_account_success"),
    path('register/', views.register, name="register"),
    path('login/', views.login_user, name="login")
]
