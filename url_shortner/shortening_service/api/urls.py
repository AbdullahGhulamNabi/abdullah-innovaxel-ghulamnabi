from django.urls import path
from .views import *

urlpatterns = [
    path('', shortener_page, name='shortener_page'),
    path('shorten/', ShortURLAPIView.as_view(), name='create_short_url'),  
    path('shorten/<str:pk>/', ShortURLAPIView.as_view(), name='retrieveUpdate_short_url'),  
    path('<str:pk>', RedirectToOriginalURL.as_view(), name='redirect-url'),
]