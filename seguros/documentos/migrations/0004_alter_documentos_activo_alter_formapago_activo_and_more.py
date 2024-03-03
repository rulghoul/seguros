# Generated by Django 4.2.10 on 2024-03-03 20:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("documentos", "0003_asesor_empresacontratante_logo_small_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="documentos",
            name="activo",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="formapago",
            name="activo",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="parentesco",
            name="activo",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="planes",
            name="activo",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="tipoconductopago",
            name="activo",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="tipomediocontacto",
            name="activo",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="tipopersona",
            name="activo",
            field=models.BooleanField(default=True),
        ),
    ]
