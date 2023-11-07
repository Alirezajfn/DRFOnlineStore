from django.db import migrations


def create_initial_categories(apps, schema_editor):
    category = apps.get_model('category', 'Category')
    user = apps.get_model('users', 'User')
    # if Category.objects.all().exists():
    #     return
    creator = user.objects.all().first()

    category.objects.create(
        name="Category 1",
        description="Description for Category 1",
        slug="category-6",
        creator=creator,
    )

    category.objects.create(
        name="Category 2",
        description="Description for Category 2",
        slug="category-5",
        creator=creator,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_initial_categories),
    ]
