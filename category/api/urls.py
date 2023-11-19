from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, add_category

app_name = 'category'

category_router = DefaultRouter()
category_router.register('', CategoryViewSet, basename='category')


urlpatterns = [
    path('add/', add_category, name='add_category'),
    path('', include(category_router.urls), name='category'),
]
