# Generated by Django 4.2.6 on 2023-11-12 09:54

from django.db import migrations

from permissions.services.get_urls import get_all_urls


def add_permissions(apps, schema_editor):
    Permission = apps.get_model('permissions', 'PermissionPerUrls')
    UrlsGroup = apps.get_model('permissions', 'UrlsGroup')
    urls = get_all_urls()
    for url in urls:
        group = None
        if url['group']:
            group, created = UrlsGroup.objects.get_or_create(name=url['group'])
        Permission.objects.create(url=url['url'],
                                  codename=url['codename'],
                                  view=url['view'],
                                  description=url['description'],
                                  app_name=url['app_name'],
                                  group=group)


def remove_permissions(apps, schema_editor):
    Permission = apps.get_model('permissions', 'PermissionPerUrls')
    UrlsGroup = apps.get_model('permissions', 'UrlsGroup')
    UrlsGroup.objects.all().delete()
    Permission.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_permissions, remove_permissions),
    ]
