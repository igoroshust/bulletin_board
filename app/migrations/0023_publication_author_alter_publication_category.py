# Generated by Django 5.0.3 on 2024-07-09 10:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_remove_publication_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.author'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='category',
            field=models.CharField(max_length=68),
        ),
    ]
