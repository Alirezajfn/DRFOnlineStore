from django.urls import get_resolver
from django.urls.resolvers import URLPattern, URLResolver

from permissions.models import UrlsGroup


def get_all_urls():

    resolver = get_resolver()
    urls = []

    def _get_urls(patterns, prefix=''):
        for pattern in patterns:
            if isinstance(pattern, URLResolver):
                _get_urls(pattern.url_patterns, prefix + pattern.pattern.regex.pattern)
            elif isinstance(pattern, URLPattern):
                if hasattr(pattern.callback, 'codename'):
                    app_name = pattern.callback.__module__.split('.')[0]
                    group_name = pattern.callback.group
                    codename = pattern.callback.codename
                    description = pattern.callback.description
                    urls.append({'url': prefix + pattern.pattern.regex.pattern,
                                 'codename': codename,
                                 'view': pattern.callback.__name__,
                                 'description': description,
                                 'app_name': app_name,
                                 'group': group_name})

    _get_urls(resolver.url_patterns)

    return urls
