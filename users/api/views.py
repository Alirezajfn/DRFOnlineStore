from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet

from users.api.serializers.register import RegisterUserSerializer
from users.api.serializers.user import UserRetrieveUpdateSerializer


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_user_model().objects.all()
    # TODO: add filter_backends

    lookup_field = 'username'
    lookup_url_kwarg = 'username'

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterUserSerializer

        return UserRetrieveUpdateSerializer

    # TODO: add change password view
