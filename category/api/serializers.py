from rest_framework import serializers

from category.api.validators import is_child_of, is_parent_exist
from category.models import Category


class CategoryCreateSerializer(serializers.ModelSerializer):
    parent = serializers.SlugField(required=False)

    class Meta:
        model = Category
        fields = [
            'name',
            'parent',
            'slug'
        ]
        read_only_fields = [
            'slug'
        ]

    def validate(self, attrs):
        parent_slug = attrs.get('parent')
        if parent_slug:
            parent = Category.objects.filter(slug=parent_slug).first()
            is_parent_exist(parent)
        return attrs

    def create(self, validated_data):
        parent_slug = validated_data.get('parent')
        if parent_slug:
            parent = Category.objects.filter(slug=parent_slug).first()
            validated_data['parent'] = parent
        else:
            validated_data['parent'] = None
        category = super().create(validated_data)
        return category


class CategoryUpdateSerializer(serializers.ModelSerializer):
    parent = serializers.SlugField(required=False)

    class Meta:
        model = Category
        fields = [
            'name',
            'parent',
            'slug'
        ]
        read_only_fields = [
            'slug'
        ]

    def validate(self, attrs):
        parent_slug = attrs.get('parent')
        if parent_slug:
            parent = Category.objects.filter(slug=parent_slug).first()
            is_parent_exist(parent)
            if parent == self.instance:
                raise serializers.ValidationError('Parent category can not be the same as the category itself')
            is_child_of(parent, self.instance)
        return attrs

    def update(self, instance, validated_data):
        parent_slug = validated_data.get('parent')
        if parent_slug:
            parent = Category.objects.filter(slug=parent_slug).first()
            validated_data['parent'] = parent
        else:
            validated_data['parent'] = None
        category = super().update(instance, validated_data)
        return category


class CategoryListSerializer(serializers.ModelSerializer):
    parent = serializers.SlugField()

    class Meta:
        model = Category
        fields = [
            'name',
            'slug',
            'parent'
        ]


class CategoryRetrieveSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    parent = serializers.SlugField()

    class Meta:
        model = Category
        fields = [
            'name',
            'slug',
            'parent',
            'children'
        ]

    def get_children(self, obj):
        children = Category.objects.filter(parent=obj)
        serializer = CategoryListSerializer(children, many=True)
        return serializer.data

