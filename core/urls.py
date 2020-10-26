from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('new/', new_post, name='new_post'),
    path('open/', open_post, name='open_post'),
    path('edit/<str:pk>/', edit_post, name='edit_post'),
    path('<str:namespace_name>/<str:pk>/', show_post_namespace, name='show_post_namespace'),
    path('<str:pk>/', show_post_no_namespace, name='show_post_no_namespace'),
    path('download/<str:pk>/', download, name="download")
]
