from django.core.management.base import BaseCommand, CommandError
from django.urls import get_resolver
from permissions.models import PermissionPerUrls, UrlsGroup


class Command(BaseCommand):
    help = 'Create permissions for all urls'

    def handle(self, *args, **options):
        resolver = get_resolver()
        urls = []

        def _get_urls(patterns, prefix=''):
            for pattern in patterns:
                if hasattr(pattern.callback, 'codename'):
                    codename = pattern.callback.codename
                    description = pattern.callback.description
                    group_name = pattern.callback.__module__.split('.')[0]
                    group, _ = UrlsGroup.objects.get_or_create(name=group_name)
                    urls.append({'url': prefix + pattern.pattern.regex.pattern,
                                 'codename': codename,
                                 'view': pattern.callback.__name__,
                                 'description': description,
                                 'group': group})
                else:
                    if hasattr(pattern, 'url_patterns'):
                        _get_urls(pattern.url_patterns, prefix + pattern.pattern.regex.pattern)

        _get_urls(resolver.url_patterns)

        PermissionPerUrls.objects.bulk_create([PermissionPerUrls(**url) for url in urls], ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS('Successfully created permissions for all urls'))
