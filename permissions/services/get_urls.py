from django.urls import get_resolver
from django.urls.resolvers import URLPattern, URLResolver


def get_all_urls():

    resolver = get_resolver()
    urls = []

    def _get_urls(patterns, prefix=''):
        for pattern in patterns:
            if isinstance(pattern, URLResolver):
                _get_urls(pattern.url_patterns, prefix + pattern.pattern.regex.pattern)
            elif isinstance(pattern, URLPattern):
                codename = ''
                if hasattr(pattern.callback, 'codename'):
                    codename = pattern.callback.codename
                if codename:
                    urls.append({'url': prefix + pattern.pattern.regex.pattern,
                                 'codename': codename,
                                 'view_name': pattern.callback.__name__})

    _get_urls(resolver.url_patterns)

    return urls
