# Generated by Django 5.1.2 on 2024-11-25 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0021_framedata_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='framedata',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='frame_data/'),
        ),
    ]
