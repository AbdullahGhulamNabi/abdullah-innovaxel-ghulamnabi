from django.urls import path
from .views import *

urlpatterns = [
    path('create/', create_short_url, name='create_short_url'),  # Correct path for 'create'
]