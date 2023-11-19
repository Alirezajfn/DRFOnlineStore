from rest_framework.response import Response

from permissions.models import PermissionPerUrls
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAdminUser

from permissions.api.serializers import PermissionReadOnlySerializer, PermissionCreateSerializer, PermissionUpdateSerializer


class PermissionListView(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    queryset = PermissionPerUrls.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'create':
            return PermissionCreateSerializer
        return PermissionReadOnlySerializer


class PermissionDetailView(mixins.DestroyModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    queryset = PermissionPerUrls.objects.filter(is_active=True)
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'update':
            return PermissionUpdateSerializer
        return PermissionReadOnlySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
