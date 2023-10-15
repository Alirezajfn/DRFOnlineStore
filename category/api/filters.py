from django_filters.rest_framework import FilterSet

from category.models import Category


class CategoryFilterSet(FilterSet):
    class Meta:
        model = Category
        fields = {
            'name': ['icontains'],
            'description': ['icontains'],
        }
