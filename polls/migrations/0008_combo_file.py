# Generated by Django 5.1.2 on 2024-11-22 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='combo',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='combos/'),
        ),
    ]
