from django.urls import path
from .views import item_list



urlpatterns = [
	path('', item_list, name='home')
]