# Generated by Django 4.2.10 on 2024-05-07 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("documentos", "0023_alter_poliza_unique_together"),
    ]

    operations = [
        migrations.RenameField(
            model_name="personaprincipal",
            old_name="clave",
            new_name="curp",
        ),
        migrations.RenameField(
            model_name="personarelacionada",
            old_name="clave",
            new_name="curp",
        ),
        migrations.AlterUniqueTogether(
            name="asesorempresa",
            unique_together={("codigo_empleado", "empresa")},
        ),
    ]