# Generated by Django 5.0.3 on 2024-07-09 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_alter_category_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publication',
            name='author',
        ),
    ]
