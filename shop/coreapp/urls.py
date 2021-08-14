from django.urls import path
from .views import checkout, item_list, products



urlpatterns = [
	path('', item_list, name='home'),
	path('products/', products, name='products'),
	path('checkout/', checkout, name='checkout'),
]