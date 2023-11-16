# Generated by Django 4.2.6 on 2023-11-12 09:54

from django.db import migrations

from permissions.services.get_urls import get_all_urls


def add_permissions(apps, schema_editor):
    Permission = apps.get_model('permissions', 'PermissionPerUrls')
    UrlsGroup = apps.get_model('permissions', 'UrlsGroup')
    urls, groups = get_all_urls()
    for group in groups:
        UrlsGroup.objects.create(name=group)
    for url in urls:
        group = UrlsGroup.objects.get(name=url['group'])
        Permission.objects.create(url=url['url'],
                                  codename=url['codename'],
                                  view=url['view'],
                                  description=url['description'],
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
