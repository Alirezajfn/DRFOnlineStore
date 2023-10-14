from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, status
from django_filters.rest_framework import DjangoFilterBackend

from product.api.filters import ProductFilterBackend, ProductFilterSet
from product.api.pagination import DynamicProductsPagination
from product.api.serializers import ProductCreateSerializer, ProductReadOnlySerializer, ProductUpdateSerializer
from product.models import Product


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
        return ProductReadOnlySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = (AllowAny,)
        else:
            # TODO: Add IsOwner permission
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


class ProductCategoryListView(ListAPIView):
    serializer_class = ProductReadOnlySerializer
    permission_classes = [AllowAny]
    pagination_class = DynamicProductsPagination
    filter_backends = (ProductFilterBackend, DjangoFilterBackend,
                       filters.OrderingFilter)
    filterset_class = ProductFilterSet
    ordering_fields = ('create_time', 'price', 'sales_count')

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        return Product.objects.filter(category__slug=category_slug)
