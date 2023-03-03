from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('test', test, name='test'),
    path('about', about, name='about_page'),
]
