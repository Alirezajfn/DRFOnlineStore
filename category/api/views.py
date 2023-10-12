from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from category.models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = (AllowAny,)
        else:
            # TODO: Add IsOwner permission
            permission_classes = (IsAdminUser,)
        return [permission() for permission in permission_classes]
