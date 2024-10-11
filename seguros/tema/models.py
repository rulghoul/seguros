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
    TRIMESTRAL = 'Q'
    SEMESTRAL = 'S'
    ANUAL = "A"

    SUBSCRIPTION_CHOICES = [
        (MENSUAL, 'Mensual'),
        (TRIMESTRAL, 'Trimestral'),
        (SEMESTRAL, 'Semestral'),
        (ANUAL, 'Anual'),
    ]

    periodos = {
        MENSUAL: 30,
        TRIMESTRAL: 90,
        SEMESTRAL: 182,
        ANUAL: 365,
    }

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=1, choices=SUBSCRIPTION_CHOICES)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.end_date:
            if self.subscription_type == self.MENSUAL:
                self.end_date = self.start_date + timedelta(days=30)
            elif self.subscription_type == self.TRIMESTRAL:
                self.end_date = self.start_date + timedelta(days=90)
            elif self.subscription_type == self.SEMESTRAL:
                self.end_date = self.start_date + timedelta(days=182)
            elif self.subscription_type == self.ANUAL:
                self.end_date = self.start_date + timedelta(years=1)
        else:
            if self.subscription_type == self.MENSUAL:
                self.end_date = self.end_date + timedelta(days=30)
            elif self.subscription_type == self.TRIMESTRAL:
                self.end_date = self.end_date + timedelta(days=90)
            elif self.subscription_type == self.SEMESTRAL:
                self.end_date = self.end_date + timedelta(days=182)
            elif self.subscription_type == self.ANUAL:
                self.end_date = self.end_date + timedelta(days=365)
        super().save(*args, **kwargs)

    def is_active(self):
        return timezone.now().date() <= self.end_date
    
    def get_dias(self):
        diferencia = self.end_date - timezone.now().date()
        return diferencia.days
    
    def is_ending(self):
        dias_diferencia = self.get_dias()
        
        if self.subscription_type == self.MENSUAL:
            umbral = 7
        elif self.subscription_type == self.TRIMESTRAL:
            umbral = 14
        else:
            umbral = 21
        # Asegúrate de que dias_diferencia no sea negativo
        if dias_diferencia <= 0:
            return True

        return dias_diferencia >= umbral
    
    def is_blocking(self):

        dias_diferencia = self.get_dias()

        if self.subscription_type == self.MENSUAL:
            umbral = -7
        elif self.subscription_type == self.TRIMESTRAL:
            umbral = -14
        else:
            umbral = -21

        return dias_diferencia < umbral
