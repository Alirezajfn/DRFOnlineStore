from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from category.models import Category
from .filters import CategoryFilterSet
from .serializers import CategoryCreateSerializer, CategoryUpdateSerializer, CategoryListSerializer, \
    CategoryRetrieveSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, )
    filterset_class = CategoryFilterSet

    def get_serializer_class(self):
        if self.action == 'create':
            return CategoryCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CategoryUpdateSerializer
        elif self.action == 'list':
            return CategoryListSerializer
        return CategoryRetrieveSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = (AllowAny,)
        else:
            # TODO: Add IsOwner permission
            permission_classes = (IsAdminUser,)
        return [permission() for permission in permission_classes]
