from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet

app_name = 'product'

product_router = DefaultRouter()
product_router.register('', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(product_router.urls), name='product'),
]
