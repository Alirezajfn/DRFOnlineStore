from rest_framework import serializers

from category.models import Category
from product.models import Product, ProductImage


class ProductCreateSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    create_time = serializers.DateTimeField(read_only=True)
    modified_time = serializers.DateTimeField(read_only=True)
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    categories = serializers.ListField(
        child=serializers.CharField(),
        required=True,
        write_only=True
    )
    categories_list = serializers.SerializerMethodField(read_only=True)
    main_image = serializers.ImageField(required=True)
    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False,
        write_only=True
    )
    images_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'stock_quantity',
            'categories',
            'creator',
            'slug',
            'create_time',
            'modified_time',
            'main_image',
            'images',
            'categories_list',
            'images_list',
        ]

    def get_categories_list(self, obj) -> list:
        return obj.categories.values_list('slug', flat=True)

    def get_images_list(self, obj) -> list:
        return obj.images.values_list('image', flat=True)

    def validate(self, attrs):
        categories = attrs.get('categories')
        for category in categories:
            if not Category.objects.filter(slug=category).exists():
                raise serializers.ValidationError('Category does not exist')

        return attrs

    def create(self, validated_data):
        """
        Create product and add categories and images to it if they are provided
        """
        category_data = validated_data.pop('categories')
        images = validated_data.pop('images', None)
        product = Product.objects.create(**validated_data)

        for category in category_data:
            category = Category.objects.filter(slug=category).first()
            if category:
                product.categories.add(category)

        if images:
            for image in images:
                ProductImage.objects.create(product=product, image=image)
        return product


class ProductUpdateSerializer(serializers.ModelSerializer):
    categories = serializers.ListField(
        child=serializers.CharField(),
        required=True,
        write_only=True
    )
    categories_list = serializers.SerializerMethodField(read_only=True)
    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False,
        write_only=True
    )
    images_list = serializers.SerializerMethodField(read_only=True)
    main_image = serializers.ImageField(required=True)

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'stock_quantity',
            'categories',
            'categories_list',
            'main_image',
            'images',
            'images_list',
        ]

    def validate(self, attrs):
        categories = attrs.get('categories')
        if categories:
            for category in categories:
                if not Category.objects.filter(slug=category).exists():
                    raise serializers.ValidationError('Category does not exist')

        return attrs

    def get_categories_list(self, obj) -> list:
        return obj.categories.values_list('slug', flat=True)

    def get_images_list(self, obj) -> list:
        return obj.images.values_list('image', flat=True)

    def update(self, instance, validated_data):
        """
        Update product and add categories and images to it if they are provided
        If categories or images is blank, delete all of them
        """
        category_data = validated_data.pop('categories', None)
        images = validated_data.pop('images', None)
        super().update(instance, validated_data)

        if category_data:
            instance.categories.clear()
            for category in category_data:
                category = Category.objects.filter(slug=category).first()
                if category:
                    instance.categories.add(category)

        if images:
            instance.images.all().delete()
            for image in images:
                ProductImage.objects.create(product=instance, image=image)
        return instance


class ProductRetrieveSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'name',
            'slug',
            'description',
            'price',
            'stock_quantity',
            'categories',
            'create_time',
            'modified_time',
            'main_image',
            'images',
            'sales_count',
        ]
        read_only_fields = fields

    def get_categories(self, obj) -> list:
        return obj.categories.values_list('slug', flat=True)

    def get_images(self, obj) -> list:
        return obj.images.values_list('image', flat=True)


class ProductListSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'name',
            'slug',
            'description',
            'price',
            'stock_quantity',
            'categories',
            'create_time',
            'modified_time',
            'main_image',
            'sales_count',
        ]
        read_only_fields = fields

    def get_categories(self, obj) -> list:
        return obj.categories.values_list('slug', flat=True)
