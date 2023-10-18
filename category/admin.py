from django.contrib import admin

from category.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'slug', 'create_time']
    list_filter = ['parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name', 'parent']
    fields = ['name', 'parent', 'description', 'slug', 'create_time', 'modified_time', 'creatorx']
    readonly_fields = ['create_time', 'modified_time']
