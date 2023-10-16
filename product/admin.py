from django.contrib import admin

from product.models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock_quantity', 'sales_count', 'is_active', 'creator', 'create_time']
    list_filter = ['is_active', 'creator']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name', 'creator']
    fields = ['name', 'slug', 'description', 'price', 'main_image', 'stock_quantity', 'sales_count', 'is_active',
              'creator', 'create_time', 'modified_time']
    readonly_fields = ['create_time', 'modified_time']
    inlines = [ProductImageInline]
