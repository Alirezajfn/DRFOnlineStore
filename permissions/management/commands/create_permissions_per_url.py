from django.core.management.base import BaseCommand, CommandError
from django.urls import get_resolver
from permissions.models import Permission


class Command(BaseCommand):
    # create_permissions_per_url command creates permissions for all urls with bulk_create
    help = 'Create permissions for all urls'

    def handle(self, *args, **options):
        resolver = get_resolver()
        urls = []

        def _get_urls(patterns, prefix=''):
            for pattern in patterns:
                if hasattr(pattern.callback, 'codename'):
                    codename = pattern.callback.codename
                    urls.append({'url': prefix + pattern.pattern.regex.pattern,
                                 'codename': codename,
                                 'view': pattern.callback.__name__})
                else:
                    if hasattr(pattern, 'url_patterns'):
                        _get_urls(pattern.url_patterns, prefix + pattern.pattern.regex.pattern)

        _get_urls(resolver.url_patterns)

        Permission.objects.bulk_create([Permission(**url) for url in urls], ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS('Successfully created permissions for all urls'))
