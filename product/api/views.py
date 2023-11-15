from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, status
from django_filters.rest_framework import DjangoFilterBackend

from permissions.services.decorators import view_permission_codename
from product.services.celery import send_mail_in_background
from product.api.filters import ProductFilterBackend, ProductFilterSet, ProductCategoryFilterBackend
from product.api.pagination import DynamicProductsPagination
from product.api.serializers import ProductCreateSerializer, ProductRetrieveSerializer, ProductUpdateSerializer, \
    ProductListSerializer
from product.models import Product
from product.services.permissions import IsSuperuserOrOwner


@extend_schema_view(
    create=extend_schema(description='Create new Product by admin.'),
    update=extend_schema(description='The admin or owner can update product details'),
    partial_update=extend_schema(description='The admin or owner can update product details'),
    destroy=extend_schema(description='The admin or owner can delete Product. '
                                      'If the product has sales, it cannot be deleted.'),
    list=extend_schema(description='The access is public. Anyone can see the list of products.'),
    retrieve=extend_schema(description='The access is public. Anyone can see the detail of a product.'),
)
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    lookup_field = 'slug'
    pagination_class = DynamicProductsPagination
    filter_backends = (ProductFilterBackend, DjangoFilterBackend,
                       filters.OrderingFilter)
    filterset_class = ProductFilterSet
    ordering_fields = ('create_time', 'price', 'sales_count')

    def get_serializer_class(self):
        if self.action == 'create':
            return ProductCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ProductUpdateSerializer
        elif self.action == 'list':
            return ProductListSerializer
        return ProductRetrieveSerializer

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

        if instance.sales_count > 0:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'detail': 'This product cannot be deleted because it has sales.'}
            )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        """
        Send email to all active admins when a new product is created
        """
        product = serializer.save()
        admins = get_user_model().objects.filter(is_superuser=True, is_active=True)
        send_mail_in_background.delay(
            to_email=[admin.email for admin in admins],
            message=f'New product added: {product.name}',
            title=f'New product added: {product.name}'
        )


@method_decorator(view_permission_codename('view_product_category_list'), name='dispatch')
class ProductCategoryListView(ListAPIView):
    """
    List of products in a category with category slug
    """
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    pagination_class = DynamicProductsPagination
    filter_backends = (ProductCategoryFilterBackend, DjangoFilterBackend,
                       filters.OrderingFilter)
    filterset_class = ProductFilterSet
    ordering_fields = ('create_time', 'price', 'sales_count')

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        return Product.objects.filter(categories__slug=category_slug)
