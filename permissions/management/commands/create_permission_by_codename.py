from django.core.management.base import BaseCommand, CommandError
from django.urls import get_resolver
from permissions.models import Permission


class Command(BaseCommand):
    help = 'Create permissions for input code name'

    def add_arguments(self, parser):
        parser.add_argument('codename', type=str, help='Code name of the permission')

    def handle(self, *args, **options):

        resolver = get_resolver()
        url = dict()

        def _get_url(patterns, prefix=''):
            for pattern in patterns:
                if hasattr(pattern.callback, 'codename'):
                    if pattern.callback.codename == options['codename']:
                        nonlocal url
                        url = {'url': prefix + pattern.pattern.regex.pattern,
                               'codename': pattern.callback.codename,
                               'view': pattern.callback.__name__}
                        return
                else:
                    if hasattr(pattern, 'url_patterns'):
                        _get_url(pattern.url_patterns, prefix + pattern.pattern.regex.pattern)

        _get_url(resolver.url_patterns)
        if url is None:
            raise CommandError('Permission does not exist.')
        else:
            Permission.objects.create(**url)
            self.stdout.write(self.style.SUCCESS('Successfully created permission for {}'.format(url['codename'])))
