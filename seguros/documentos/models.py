from django.contrib.auth.models import User
from django.db import models

from django_ckeditor_5.fields import CKEditor5Field
from simple_history.models import HistoricalRecords



######################### Opciones ###########################

OPCIONES_GENERO = [
    ('H', 'Hombre'),
    ('M', 'Mujer'),
    ('O', 'Otro'),
    ]

OPCIONES_BOLEANO = [('S','Si'),('N',"No"),('I','Incompleto')]

STATUS_PLAN = [('TERMINADO'),]

STATUS_SEGURO_VIDA = [('PGD','PAGADO'),('PEN','PEDIENTE DE PAGO'), ("EN PROCESO"), ("CANCELADO")]

STATUS_GASTOS_MEDICOS = [('PGD','PAGADO'),('PEN','PEDIENTE DE PAGO'), ("EN PROCESO")]

STATUS_PERSONA = [("A","ACTIVO"),("I","INACTIVO")]

TIPO_PERSONA = ("CLIENTE", "BENEFICIARIO")

class Asesor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono1 = models.CharField(max_length=20)
    telefono2 = models.CharField(max_length=20)
    history = HistoricalRecords()


######################### Catalogos ###########################

class TipoConductoPago(models.Model):
    clave = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    activo = models.BooleanField(default=True)
    history = HistoricalRecords()


class TipoPersona(models.Model):
    clave = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    history = HistoricalRecords()

class FormaPago(models.Model): #("CLIENTE", "BENEFICIARIO")
    clave = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    activo = models.BooleanField(default=True)
    history = HistoricalRecords()

class Documentos(models.Model):
    clave = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    activo = models.BooleanField(default=True)
    history = HistoricalRecords()


class TipoMediocontacto(models.Model):
    descripcion = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)
    history = HistoricalRecords()


class Parentesco(models.Model):
    descripcion = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)
    history = HistoricalRecords()


######## Tablas Principales ############

class EmpresaContratante(models.Model):
    clave = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    activo = models.IntegerField(default = True)
    logo_small = models.FileField(blank=True, null=True, default=None)
    pleca = models.FileField(blank=True, null=True, default=None)
    history = HistoricalRecords()

class AsesorEmpresa(models.Model):
    empresa = models.ForeignKey(EmpresaContratante, on_delete=models.CASCADE)
    asesor = models.ForeignKey(Asesor, on_delete=models.CASCADE)
    history = HistoricalRecords()

class Planes(models.Model):
    clave = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    empresa = models.ForeignKey(EmpresaContratante, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)
    history = HistoricalRecords()

class PersonaBase(models.Model):
    clave = models.CharField(max_length=20)
    tipo_persona = models.ForeignKey(TipoPersona, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=80)  # Asegúrate de que el max_length sea suficiente para ambos casos
    primer_apellido = models.CharField(max_length=120)
    segundo_apellido = models.CharField(max_length=120, blank=True, null=True)
    genero = models.CharField(max_length=1, choices=OPCIONES_GENERO)
    estatus = models.CharField(max_length=10) ## Hay catalogo de estatus de personas?
    history = HistoricalRecords()

    class Meta:
        abstract = True

class PersonaPrincipal(PersonaBase):  
    lugar_nacimiento = models.CharField( max_length=50, blank=True, null=True)  
    fecha_nacimiento = models.DateTimeField()   
    history = HistoricalRecords()

class PersonaRelacionada(PersonaBase):
    parentesco = models.ForeignKey(Parentesco, on_delete=models.CASCADE)
    persona_principal = models.ForeignKey(PersonaPrincipal, on_delete=models.CASCADE) 
    history = HistoricalRecords()

class Poliza(models.Model):
    empresa = models.ForeignKey(EmpresaContratante, on_delete=models.CASCADE)
    asesor = models.ForeignKey(Asesor, on_delete=models.CASCADE)
    numero_poliza = models.CharField(max_length=25)  
    persona_principal =  models.ForeignKey(PersonaPrincipal, on_delete=models.CASCADE) 
    forma_pago = models.ForeignKey(FormaPago, on_delete=models.CASCADE)  
    tipo_conducto_pago = models.ForeignKey(TipoConductoPago, on_delete=models.CASCADE) 
    plan = models.ForeignKey(Planes, on_delete=models.CASCADE)    
    fechavigencia = models.DateTimeField()  
    estatus = models.CharField( max_length=10)  ## Hay catalogo de estatus de polizas?
    history = HistoricalRecords()

class Beneficiarios(models.Model):
    numero_poliza = models.ForeignKey(Poliza, on_delete=models.CASCADE)  
    persona_relacionada = models.ForeignKey(PersonaRelacionada, on_delete=models.CASCADE) 
    tipo_persona = models.ForeignKey(TipoPersona, on_delete=models.CASCADE) 
    #persona_principal = models.CharField( max_length=20)  
    porcentaje_participacion = models.PositiveSmallIntegerField( blank=True, null=True)  
    history = HistoricalRecords()

class CheckDocumentos(models.Model):
    numero_poliza = models.ForeignKey(Poliza, on_delete=models.CASCADE)  
    plan = models.ForeignKey(Planes, on_delete=models.CASCADE)
    empresa = models.ForeignKey(EmpresaContratante, on_delete=models.CASCADE)
    documento = models.ForeignKey(Documentos,on_delete=models.CASCADE)
    necesario = models.CharField(max_length=1,choices=OPCIONES_BOLEANO)
    entregado = models.CharField(max_length=1,choices=OPCIONES_BOLEANO)
    archivo = models.FileField()
    fecha_adjuntado = models.DateTimeField()  
    history = HistoricalRecords()


class PlanDocumentos(models.Model):
    clave = models.CharField(max_length=20)
    empresa = models.ForeignKey(EmpresaContratante, on_delete=models.CASCADE)
    documento = models.ForeignKey(Documentos, on_delete=models.CASCADE)
    history = HistoricalRecords()

class Siniestros(models.Model):
    poliza = models.ForeignKey(Poliza,on_delete=models.CASCADE)
    numero_siniestro = models.PositiveSmallIntegerField( blank=True, null=True)  
    descripcion_siniestro = models.CharField(max_length=500, blank=True, null=True)  
    fecha_evento = models.DateTimeField()  
    estatus = models.CharField(max_length=10)
    history = HistoricalRecords()

