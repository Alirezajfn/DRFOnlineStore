from permissions.models import PermissionPerUrls, UrlsGroup, Role
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
        # if group does not exist, it will be created
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

    # if group does not exist, it will be created
    def update(self, instance, validated_data):
        group_name = validated_data.pop('group', None)
        if group_name:
            group, _ = UrlsGroup.objects.get_or_create(name=group_name)
            validated_data['group'] = group
        return super().update(instance, validated_data)


class RoleReadOnlySerializer(serializers.ModelSerializer):
    permissions = serializers.StringRelatedField(many=True)

    class Meta:
        model = Role
        fields = (
            'id',
            'name',
            'permissions',
        )


class RoleCreateSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField(child=serializers.CharField(max_length=255), required=False)

    class Meta:
        model = Role
        fields = (
            'id',
            'name',
            'permissions',
        )

    def validate(self, attrs):
        permissions = attrs.get('permissions', None)
        if permissions:
            for permission in permissions:
                if not PermissionPerUrls.objects.filter(codename=permission).exists():
                    raise serializers.ValidationError(f"Permission {permission} does not exist")
        return attrs

    def create(self, validated_data):
        permissions = validated_data.pop('permissions', None)
        role = super().create(validated_data)
        if permissions:
            for permission in permissions:
                permission_obj = PermissionPerUrls.objects.get(codename=permission)
                role.permissions.add(permission_obj)
        return role

    def to_representation(self, instance):
        self.fields['permissions'] = PermissionReadOnlySerializer(many=True)
        return super().to_representation(instance)


class RoleUpdateSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField(child=serializers.CharField(max_length=255), required=False)

    class Meta:
        model = Role
        fields = (
            'id',
            'name',
            'permissions',
        )

    def validate(self, attrs):
        permissions = attrs.get('permissions', None)
        if permissions:
            for permission in permissions:
                if not PermissionPerUrls.objects.filter(codename=permission).exists():
                    raise serializers.ValidationError(f"Permission {permission} does not exist")
        return attrs

    def update(self, instance, validated_data):
        permissions = validated_data.pop('permissions', None)
        role = super().update(instance, validated_data)
        if permissions:
            role.permissions.clear()
            for permission in permissions:
                permission_obj = PermissionPerUrls.objects.get(codename=permission)
                role.permissions.add(permission_obj)
        return role

    def to_representation(self, instance):
        self.fields['permissions'] = PermissionReadOnlySerializer(many=True)
        return super().to_representation(instance)
