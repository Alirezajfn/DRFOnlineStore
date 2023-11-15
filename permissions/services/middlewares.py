from django.contrib.auth.middleware import get_user
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseForbidden
from django.urls import resolve
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken

from permissions.models import Permission


class URLPermissionCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        resolver_match = resolve(request.path_info)
        if hasattr(resolver_match.func, 'codename'):
            codename = resolver_match.func.codename
        else:
            return self.get_response(request)

        user = self.get_jwt_user(request)

        if codename is not None:
            try:
                permission = Permission.objects.get(codename=codename)
            except Permission.DoesNotExist:
                return HttpResponseForbidden("Permission does not exist.")
            else:
                if not user.permissions_per_url.filter(pk=permission.pk).exists():
                    return HttpResponseForbidden("Permission denied.")
        return self.get_response(request)

    @staticmethod
    def get_jwt_user(request):
        user = get_user(request)
        if user.is_authenticated:
            return user
        try:
            user = authentication.JWTAuthentication().authenticate(request)[0]
        except AuthenticationFailed:
            user = AnonymousUser()
        return user
        # jwt_authentication = JWTAuthentication()
        # try:
        #     print(request.headers.get('Authorization'))
        #     jwt = AccessToken(request.headers.get('Authorization').split()[1])
        #     user = jwt_authentication.get_user(jwt)
        # except AuthenticationFailed:
        #     user = AnonymousUser()
        # return user
