# Generated by Django 4.2.6 on 2023-11-12 09:54

from django.db import migrations

from permissions.services.get_urls import get_all_urls


def add_permissions(apps, schema_editor):
    Permission = apps.get_model('permissions', 'Permission')
    for url in get_all_urls():
        Permission.objects.create(codename=url['codename'], url=url['url'], view=url['view_name'])


def remove_permissions(apps, schema_editor):
    Permission = apps.get_model('permissions', 'Permission')
    Permission.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_permissions, remove_permissions),
    ]
