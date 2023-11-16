from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from permissions.models import PermissionPerUrls


class UserRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]

        extra_kwargs = {
            'email': {'read_only': True},
            'last_login': {'read_only': True},
        }

    def validate(self, attrs):
        username = attrs.get('username', None)
        if username:
            exists = get_user_model().objects.filter(username=username).exists()
            if exists:
                ValidationError(_('Chosen Username Exists'))

        return attrs


class PermissionReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionPerUrls
        fields = [
            'codename',
            'name',
        ]
        extra_kwargs = {
            'codename': {'read_only': True},
            'name': {'read_only': True},
        }


class GroupReadOnlySerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Group
        fields = [
            'name',
            'permissions',

        ]
        extra_kwargs = {
            'groups': {'read_only': True},
            'permissions': {'read_only': True},
        }

    def get_permissions(self, obj):
        return obj.permissions.values_list('codename', flat=True)


class UserPermissionSerializer(serializers.Serializer):
    permissions = serializers.ListField(child=serializers.CharField(max_length=255), required=False)
    groups = serializers.ListField(child=serializers.CharField(max_length=255), required=False)

    def validate(self, attrs):
        permissions = attrs.get('permissions', [])
        groups = attrs.get('groups', [])

        for perm in permissions:
            if not PermissionPerUrls.objects.filter(codename=perm).exists():
                raise serializers.ValidationError("Permission does not exist.")

        for group in groups:
            if not Group.objects.filter(name=group).exists():
                raise serializers.ValidationError("Group does not exist.")

        return attrs
