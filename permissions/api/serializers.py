from permissions.models import PermissionPerUrls
from rest_framework import serializers


class PermissionListSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField()

    class Meta:
        model = PermissionPerUrls
        fields = (
            'id',
            'url',
            'codename',
            'view',
            'is_active',
            'description',
            'group',
        )
