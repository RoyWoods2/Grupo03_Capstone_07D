# Generated by Django 5.1.2 on 2024-11-13 00:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_framedata'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('imagen', models.ImageField(upload_to='hub_images/')),
                ('juego', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.juego')),
            ],
        ),
    ]