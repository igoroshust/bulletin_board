# Generated by Django 5.0.3 on 2024-07-08 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_alter_category_name_alter_publication_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='category',
            field=models.CharField(choices=[('AP', 'Обращение'), ('CP', 'Жалоба')], default='AP', max_length=2),
        ),
    ]
