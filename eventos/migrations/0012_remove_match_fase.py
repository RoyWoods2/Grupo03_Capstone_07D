# Generated by Django 5.1.2 on 2024-12-01 03:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("eventos", "0011_match_fase"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="match",
            name="fase",
        ),
    ]
