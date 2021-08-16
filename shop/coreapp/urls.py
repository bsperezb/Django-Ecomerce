from django.urls import path
from .views import (checkout, HomeView, ItemDetailView, add_to_cart, remove_from_cart )

app_name = 'coreapp'

urlpatterns = [
	path('', HomeView.as_view(), name='home'),
	path('product/<slug>/', ItemDetailView.as_view() , name='product'),
	path('checkout/', checkout, name='checkout'),
	path('checkout/', checkout, name='checkout'),
	path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
	path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
]