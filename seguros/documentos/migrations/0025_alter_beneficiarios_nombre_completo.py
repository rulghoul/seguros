# Generated by Django 4.2.10 on 2024-05-07 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("documentos", "0024_rename_clave_personaprincipal_curp_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="beneficiarios",
            name="nombre_completo",
            field=models.CharField(max_length=100),
        ),
    ]
