from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.api.views import UserViewSet, UserPermissionView, GetAllPermissionsView

app_name = 'users'

router = DefaultRouter()
router.register('', UserViewSet, basename='user')

urlpatterns = [
    path('permissions/<str:username>/', UserPermissionView.as_view(), name='user_permissions'),
    path('get_permissions/', GetAllPermissionsView.as_view(), name='get_permissions'),
    path('', include(router.urls), name='users'),
]
