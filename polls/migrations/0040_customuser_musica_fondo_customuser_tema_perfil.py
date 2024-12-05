# Generated by Django 5.1.2 on 2024-12-04 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0039_moderacion"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="musica_fondo",
            field=models.URLField(
                blank=True, help_text="URL de música de fondo", null=True
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="tema_perfil",
            field=models.CharField(
                choices=[
                    ("dark", "Oscuro"),
                    ("light", "Claro"),
                    ("retro", "Retro"),
                    ("arcade", "Arcade"),
                ],
                default="dark",
                max_length=50,
            ),
        ),
    ]
