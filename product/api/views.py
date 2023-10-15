from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, status
from django_filters.rest_framework import DjangoFilterBackend

from product.services.celery import send_mail_in_background
from product.api.filters import ProductFilterBackend, ProductFilterSet, ProductCategoryFilterBackend
from product.api.pagination import DynamicProductsPagination
from product.api.serializers import ProductCreateSerializer, ProductRetrieveSerializer, ProductUpdateSerializer, \
    ProductListSerializer
from product.models import Product
from product.services.permissions import IsSuperuserOrOwner


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
        product = serializer.save()
        admins = get_user_model().objects.filter(is_superuser=True, is_active=True)
        send_mail_in_background.delay(
            to_email=[admin.email for admin in admins],
            message=f'New product added: {product.name}',
            title=f'New product added: {product.name}'
        )


class ProductCategoryListView(ListAPIView):
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
