from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from category.models import Category
from product.services.permissions import IsSuperuserOrOwner
from .filters import CategoryFilterSet
from .serializers import CategoryCreateSerializer, CategoryUpdateSerializer, CategoryListSerializer, \
    CategoryRetrieveSerializer


@extend_schema_view(
    create=extend_schema(description='Create new Category with name, slug, '
                                     'description and parent slug by admin'),
    update=extend_schema(description='The admin or owner can update name, '
                                     'parent slug and description of Category'),
    partial_update=extend_schema(description='The admin or owner can update name, '
                                             'parent slug and description of Category'),
    destroy=extend_schema(description='The admin or owner can delete Category. '
                                      'If the category has product, it cannot be deleted.'),
    list=extend_schema(description='The access is public. Anyone can see the list of categories.'),
    retrieve=extend_schema(description='The access is public. Anyone can see the detail of a category.'),
)
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
        if self.request.user.has_perm('category.add_category'):
            return []
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
