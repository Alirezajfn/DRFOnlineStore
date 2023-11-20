from django.urls import path

from .views import PermissionListView, PermissionDetailView, RoleListView, RoleDetailView

app_name = 'permission'

urlpatterns = [
    path('', PermissionListView.as_view({'post': 'create', 'get': 'list'}), name='permission-list'),
    path('<int:pk>/', PermissionDetailView.as_view({'delete': 'destroy', 'put': 'update', 'get': 'retrieve'}), name='permission-detail'),
    path('role/', RoleListView.as_view({'post': 'create', 'get': 'list'}), name='role-list'),
    path('role/<int:pk>/', RoleDetailView.as_view({'put': 'update', 'get': 'retrieve'}), name='role-detail'),

]
