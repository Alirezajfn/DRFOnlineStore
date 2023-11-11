from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from drf_spectacular.utils import extend_schema_view, extend_schema

from rest_framework import mixins
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from users.api.filters import SelfFilterBacked
from users.api.serializers.register import RegisterUserSerializer
from users.api.serializers.user import UserRetrieveUpdateSerializer, UserPermissionSerializer, \
    PermissionReadOnlySerializer, GroupReadOnlySerializer


@extend_schema_view(
    retrieve=extend_schema(description='The retrieve action is used to retrieve a user by username'),
    update=extend_schema(description='The update action is used to update the information of each user by '
                                     'himself with all the fields'),
    partial_update=extend_schema(description='The partial update action is used to update the information'
                                             ' of each user by himself with some of the fields'),
    create=extend_schema(description='The create action is used to register a new user with all the fields'),
)
class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_user_model().objects.all()
    filter_backends = [SelfFilterBacked]

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


class UserPermissionView(GenericAPIView):
    serializer_class = UserPermissionSerializer
    permission_classes = [IsAdminUser]

    def post(self, request, username):
        user = get_user_model().objects.get(username=username)
        serializer = UserPermissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        permissions = Permission.objects.filter(codename__in=serializer.validated_data['permissions'])
        user.user_permissions.set(permissions)
        groups = Group.objects.filter(name__in=serializer.validated_data['groups'])
        user.groups.set(groups)
        return Response({'message': 'Permissions changed successfully'})


class GetAllPermissionsView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = PermissionReadOnlySerializer
    queryset = Permission.objects.all()


class GetAllGroupsView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = GroupReadOnlySerializer
    queryset = Group.objects.all()
