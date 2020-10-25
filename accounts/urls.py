from django.urls import path

from accounts import views

app_name = "accounts"

urlpatterns = [
    path('', views.home, name="home"),
    path('posts/', views.posts, name="posts"),
    path('namespaces/', views.namespaces, name="namespaces"),
    path('settings', views.settings, name="settings"),
    path('register/', views.register, name="register")
]