# Generated by Django 4.2.10 on 2024-08-06 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tema", "0004_alter_parametros_imagenes_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="parametros_imagenes",
            name="title",
            field=models.CharField(
                choices=[
                    ("logo", "Logo de pleca"),
                    ("bigLogo", "Logo de Login"),
                    ("fondo", "Background "),
                    ("agencia", "Logo de la agencia"),
                    ("happy", "Imagen de cumpleaños"),
                ],
                default="logo",
                max_length=60,
                unique=True,
            ),
        ),
    ]
