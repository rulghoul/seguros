# Generated by Django 4.2.10 on 2024-08-09 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("documentos", "0046_remove_planes_clave"),
    ]

    operations = [
        migrations.AlterField(
            model_name="poliza",
            name="estatus",
            field=models.CharField(
                choices=[
                    ("PGD", "PAGADO"),
                    ("PEN", "PEDIENTE DE PAGO"),
                    ("EPR", "EN PROCESO"),
                    ("CAN", "CANCELADO"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="siniestros",
            name="estatus",
            field=models.CharField(
                choices=[
                    ("PGD", "PAGADO"),
                    ("PEN", "PEDIENTE DE PAGO"),
                    ("EPR", "EN PROCESO"),
                    ("CAN", "CANCELADO"),
                ],
                max_length=10,
            ),
        ),
    ]
