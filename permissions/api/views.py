from rest_framework.response import Response

from permissions.models import PermissionPerUrls
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAdminUser

from permissions.api.serializers import PermissionListSerializer


class PermissionListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PermissionListSerializer
    queryset = PermissionPerUrls.objects.all()
    permission_classes = [IsAdminUser]


class PermissionDestroyView(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = PermissionPerUrls.objects.filter(is_active=True)
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
