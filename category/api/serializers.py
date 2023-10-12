from rest_framework import serializers

from category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.SlugField(allow_null=True, allow_blank=True)
    children = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = [
            'name',
            'parent',
        ]

    def validate(self, attrs):
        if attrs['parent']:
            parent = Category.objects.filter(slug=attrs['parent']).first()
            if not parent:
                raise serializers.ValidationError('Parent category not found')
            if parent == self.instance:
                raise serializers.ValidationError('Parent category can not be the same as category itself')
        return attrs

    def get_children(self, obj):
        children = obj.children.all()
        serializer = CategorySerializer(children, many=True)
        return serializer.data

    def create(self, validated_data):
        if validated_data['parent']:
            parent = Category.objects.filter(slug=validated_data['parent']).first()
            validated_data['parent'] = parent
        else:
            validated_data['parent'] = None
        category = super().create(validated_data)
        return category

    def update(self, instance, validated_data):
        if validated_data['parent']:
            parent = Category.objects.filter(slug=validated_data['parent']).first()
            validated_data['parent'] = parent
        else:
            validated_data['parent'] = None
        category = super().update(instance, validated_data)
        return category
