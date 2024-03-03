# Generated by Django 4.2.10 on 2024-03-03 18:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "documentos",
            "0002_rename_feccha_nacimiento_personaprincipal_fecha_nacimiento_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Asesor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("telefono1", models.CharField(max_length=20)),
                ("telefono2", models.CharField(max_length=20)),
                (
                    "usuario",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="empresacontratante",
            name="logo_small",
            field=models.FileField(blank=True, default=None, null=True, upload_to=""),
        ),
        migrations.AddField(
            model_name="empresacontratante",
            name="pleca",
            field=models.FileField(blank=True, default=None, null=True, upload_to=""),
        ),
        migrations.AddField(
            model_name="personarelacionada",
            name="parentesco",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="documentos.parentesco",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="checkdocumentos",
            name="plan",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="documentos.planes"
            ),
        ),
        migrations.CreateModel(
            name="AsesorEmpresa",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "asesor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="documentos.asesor",
                    ),
                ),
                (
                    "empresa",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="documentos.empresacontratante",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="poliza",
            name="asesor",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="documentos.asesor",
            ),
            preserve_default=False,
        ),
    ]
