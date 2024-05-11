# Generated by Django 4.2.10 on 2024-05-11 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("documentos", "0029_alter_beneficiarios_parentesco"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="plandocumentos",
            name="clave",
        ),
        migrations.AddField(
            model_name="planes",
            name="siniestros",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name="beneficiarios",
            unique_together={("numero_poliza", "parentesco")},
        ),
    ]
