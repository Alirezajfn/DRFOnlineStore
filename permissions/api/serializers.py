from permissions.models import PermissionPerUrls, UrlsGroup
from rest_framework import serializers


class PermissionReadOnlySerializer(serializers.ModelSerializer):
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
            'app_name',
            'group',
        )
        read_only_fields = fields


class PermissionCreateSerializer(serializers.ModelSerializer):
    group = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = PermissionPerUrls
        fields = (
            'id',
            'url',
            'codename',
            'view',
            'is_active',
            'description',
            'app_name',
            'group',
        )
        read_only_fields = (
            'id',
            'view',
            'is_active',
            'app_name',
        )

    def create(self, validated_data):
        group_name = validated_data.pop('group', None)
        if group_name:
            group, _ = UrlsGroup.objects.get_or_create(name=group_name)
            validated_data['group'] = group
        return super().create(validated_data)


class PermissionUpdateSerializer(serializers.ModelSerializer):
    group = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = PermissionPerUrls
        fields = (
            'id',
            'url',
            'codename',
            'view',
            'is_active',
            'description',
            'app_name',
            'group',
        )
        read_only_fields = (
            'id',
            'view',
            'is_active',
            'app_name',
        )

    def update(self, instance, validated_data):
        group_name = validated_data.pop('group', None)
        if group_name:
            group, _ = UrlsGroup.objects.get_or_create(name=group_name)
            validated_data['group'] = group
        return super().update(instance, validated_data)
