from django.urls import path

from .views import PermissionListView, PermissionDestroyView


app_name = 'permission'

urlpatterns = [
    path('', PermissionListView.as_view({'get': 'list'}), name='permission-list'),
    path('<int:pk>/', PermissionDestroyView.as_view({'delete': 'destroy'}), name='permission-destroy'),

]
