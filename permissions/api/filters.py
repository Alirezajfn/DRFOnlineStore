from django_filters.rest_framework import FilterSet

from permissions.models import PermissionPerUrls


class PermissionFilterSet(FilterSet):
    class Meta:
        model = PermissionPerUrls
        fields = {
            'codename': ['exact', 'icontains'],
            'url': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
            'app_name': ['exact', 'icontains'],
            'group__name': ['exact', 'icontains'],
        }
