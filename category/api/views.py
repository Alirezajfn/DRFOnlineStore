from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from category.models import Category
from product.services.permissions import IsSuperuserOrOwner
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
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = (IsSuperuserOrOwner,)
        else:
            permission_classes = (IsAdminUser,)
        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
        except:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'detail': 'This category cannot be deleted because it has product.'}
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
