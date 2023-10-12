from django.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework.urls import path

from .views import CategoryViewSet

app_name = 'category'

category_router = DefaultRouter()
category_router.register('', CategoryViewSet, basename='user')


urlpatterns = [
    category_router.urls
]
