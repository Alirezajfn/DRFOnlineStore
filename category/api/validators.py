from rest_framework import serializers

from category.models import Category


def is_child_of(parent: Category, child: Category) -> None:
    """
    Check if parent is child of itself raise ValidationError
    """
    if parent.parent:
        if parent.parent == child:
            raise serializers.ValidationError('Parent category can not be the same as the category itself')
        is_child_of(parent.parent, child)


def is_parent_exist(parent: Category) -> None:
    """
    Check if parent is not exist raise ValidationError
    """
    if not parent:
        raise serializers.ValidationError('Parent category not found')
