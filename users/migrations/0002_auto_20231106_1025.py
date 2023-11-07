from django.db import migrations
from django.contrib.auth import get_user_model


def create_initial_users(apps, schema_editor):
    user = apps.get_model(get_user_model())
    user.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin',
    )
    user.objects.create_user(
        username='user',
        email='user@example.com',
        password='user',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_initial_users),
    ]
