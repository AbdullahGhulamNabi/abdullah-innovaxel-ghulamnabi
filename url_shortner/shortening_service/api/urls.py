from django.urls import path
from .views import *

urlpatterns = [
    path('', shortener_page, name='shortener_page'),
    path('shorten/', ShortURLAPIView.as_view(), name='create-shorturl'),  
    path('shorten/<str:pk>/', ShortURLAPIView.as_view(), name='retrieveUpdateDelete-short-url'),  
    path('stats/<str:pk>/', StatsURLAPIView.as_view(), name='stats-short-url'),  
    path('<str:pk>', RedirectToOriginalURL.as_view(), name='redirect-url'),
]