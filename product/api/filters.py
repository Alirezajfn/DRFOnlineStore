from django_filters.rest_framework import FilterSet
from rest_framework.filters import BaseFilterBackend

from product.models import Product


class ProductFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(is_active=True)


class ProductFilterSet(FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['icontains'],
            'description': ['icontains'],
            'price': ['gte', 'lte'],
            'stock_quantity': ['gte', 'lte'],
            'create_time': ['gte', 'lte'],
            'sales_count': ['gte', 'lte'],
        }
