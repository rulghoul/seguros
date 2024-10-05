from django.db import models
from simple_history.models import HistoricalRecords
from colorfield.fields import ColorField
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

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
    ('agencia', 'Logo de la agencia'), 
    ('happy', 'Imagen de cumpleaños'), 
]

class parametros_imagenes(models.Model):
    title = models.CharField(max_length=60, choices=TITLE_CHOICES, default='logo', unique=True)
    image = models.ImageField(upload_to='images_parameter')

    def __str__(self):
        return self.title
    
class Subscription(models.Model):
    MENSUAL = 'M'
    TRIMISTRAL = 'Q'
    SEMESTRAL = 'S'
    ANUAL = "A"
    SUBSCRIPTION_CHOICES = [
        (MENSUAL, 'Mensual'),
        (TRIMISTRAL, 'Trimestral'),
        (SEMESTRAL, 'Semestral'),
        (ANUAL, 'Anual'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=1, choices=SUBSCRIPTION_CHOICES)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.end_date:
            if self.subscription_type == self.MONTHLY:
                self.end_date = self.start_date + timedelta(days=30)
            elif self.subscription_type == self.QUARTERLY:
                self.end_date = self.start_date + timedelta(days=90)
            elif self.subscription_type == self.SEMIANNUAL:
                self.end_date = self.start_date + timedelta(days=180)
        super().save(*args, **kwargs)

    def is_active(self):
        return timezone.now() <= self.end_date