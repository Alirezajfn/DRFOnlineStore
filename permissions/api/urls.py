from django.urls import path

from .views import PermissionListView, PermissionDetailView

app_name = 'permission'

urlpatterns = [
    path('', PermissionListView.as_view({'post': 'create', 'get': 'list'}), name='permission-list'),
    path('<int:pk>/', PermissionDetailView.as_view({'delete': 'destroy', 'put': 'update', 'get': 'retrieve'}), name='permission-detail'),

]
