from django.urls import path
from .views import index , delete_city

urlpatterns = [
    path('', index, name='index'),
    path('delete_city/<int:city_id>/', delete_city, name='delete_city'),
]
