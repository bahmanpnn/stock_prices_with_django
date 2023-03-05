from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('test', test, name='test'),
    path('about', about, name='about_page'),
    path('stock', stocks, name='stock_page'),
    path('delete/<stock_symbol>', delete_stock, name='delete_stock'),
]
