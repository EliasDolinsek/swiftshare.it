from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('new/', new_post, name='new_post'),
    path('edit/<str:pk>', edit_post, name='edit_post'),
    path('<str:pk>/', show_post, name='show_post')
]
