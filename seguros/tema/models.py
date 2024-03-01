from django.db import models
from simple_history.models import HistoricalRecords
from colorfield.fields import ColorField

COLOR_CHOICES = [
    ('pleca', 'Color de pleca'),
    ('menu', 'Color de menu'),
    ('fondo', 'Color de fondo'),
]

class parametros_colores(models.Model):
    elemento = models.CharField(db_column='elemento', max_length=50,choices=COLOR_CHOICES, default="pleca"
                                , unique=True, blank=False, null=False)
    color = ColorField(default='#FF0000')

    class Meta:
        db_table = 'parametros_colores'

TITLE_CHOICES = [
    ('logo', 'Logo de pleca'),
    ('bigLogo', 'Logo de Login'),
    ('fondo', 'Background '), 
]

class parametros_imagenes(models.Model):
    title = models.CharField(max_length=60, choices=TITLE_CHOICES, default='logo', unique=True)
    image = models.ImageField(upload_to='images_parameter')

    def __str__(self):
        return self.title