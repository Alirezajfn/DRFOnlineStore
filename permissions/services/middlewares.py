from django.contrib.auth.middleware import get_user
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseForbidden
from django.urls import resolve
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from permissions.models import Permission


class URLPermissionCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = self.get_jwt_user(request)
        resolver_match = resolve(request.path_info)
        if hasattr(resolver_match.func, 'codename'):
            codename = resolver_match.func.codename
        else:
            codename = resolver_match.url_name
        if codename is not None:
            try:
                # permission = Permission.objects.get(codename=codename)
                permission = Permission.objects.filter(codename=codename).first()
            except Permission.DoesNotExist:
                return HttpResponseForbidden("Permission does not exist.")
            else:
                if not user.permissions_per_url.filter(pk=permission.pk).exists():
                    return HttpResponseForbidden("Permission denied.")
                print("Permission granted.")
        return self.get_response(request)

    @staticmethod
    def get_jwt_user(request):
        user = get_user(request)
        if user.is_authenticated:
            return user
        jwt_authentication = JWTAuthentication()
        try:
            user, jwt = jwt_authentication.authenticate(request)
        except AuthenticationFailed:
            user = AnonymousUser()
        return user
