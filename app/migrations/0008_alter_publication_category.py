# Generated by Django 5.0.3 on 2024-09-01 02:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_publication_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='category',
            field=models.ForeignKey(choices=[('tank', 'Танки'), ('heal', 'Хилы'), ('dd', 'ДД'), ('merchant', 'Торговцы'), ('gildmasters', 'Гилдмастеры'), ('quest', 'Квестгиверы'), ('smith', 'Кузнецы'), ('tanner', 'Кожевники'), ('potion', 'Зельевары'), ('spellmaster', 'Мастера заклинаний'), ('unknown', 'Без категории')], on_delete=django.db.models.deletion.CASCADE, related_name='publications', to='app.category'),
        ),
    ]
