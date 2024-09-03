# Generated by Django 5.0.3 on 2024-09-03 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_response_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='status',
            field=models.CharField(choices=[('pending', 'отправлено'), ('hide', 'удалено'), ('deleted', 'отклонено'), ('accepted', 'принято')], default='pending', max_length=20),
        ),
    ]
