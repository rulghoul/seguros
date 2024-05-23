from django.contrib.auth.models import User
from django.db import models

from django_ckeditor_5.fields import CKEditor5Field
from simple_history.models import HistoricalRecords

from sepomex import models as sepomex

######################### Opciones ###########################

OPCIONES_GENERO = [
    ('H', 'Hombre'),
    ('M', 'Mujer'),
    ('O', 'Otro'),
    ]

OPCIONES_BOLEANO = [('S','Si'),('N',"No"),('I','Incompleto')]

STATUS_PLAN = [('TERMINADO'),]

STATUS_SEGURO_VIDA = [('PGD','PAGADO'),('PEN','PEDIENTE DE PAGO'), ("EN PROCESO"), ("CANCELADO")]

STATUS_GASTOS_MEDICOS = [('PGD','PAGADO'),('PEN','PEDIENTE DE PAGO'), ('EPR','EN PROCESO')]

STATUS_PERSONA = [("A","ACTIVO"),("I","INACTIVO")]

TIPO_PERSONA = ("CLIENTE", "BENEFICIARIO")

############### Campo personalizado #####################

class ClaveField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20  # Tamaño máximo de 20
        kwargs['null'] = False  # No permite valores nulos
        kwargs['blank'] = False  # No permite cadenas vacías
        kwargs['unique'] = True  # Hace que el campo sea único por defecto
        super().__init__(*args, **kwargs)


######################### Catalogos ###########################

class TipoConductoPago(models.Model):
    clave = ClaveField()
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    activo = models.BooleanField(default=True)
    

    def __str__(self) -> str:
        return self.descripcion


class TipoPersona(models.Model):
    clave = ClaveField()
    descripcion = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    

    def __str__(self) -> str:
        return self.descripcion

class FormaPago(models.Model): #("CLIENTE", "BENEFICIARIO")
    clave = ClaveField()
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.descripcion

class Documentos(models.Model):
    clave = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.descripcion


class TipoMediocontacto(models.Model):
    descripcion = models.CharField(max_length=20, unique=True)
    activo = models.BooleanField(default=True)
    
    
    def __str__(self) -> str:
        return self.descripcion


class Parentesco(models.Model):
    descripcion = models.CharField(max_length=20, unique=True)
    activo = models.BooleanField(default=True)
    
    
    def __str__(self) -> str:
        return self.descripcion


######## Tablas Principales ############

class EmpresaContratante(models.Model):
    clave = ClaveField()
    nombre = models.CharField(max_length=100, blank=True, null=True)
    logo_small = models.ImageField(upload_to='empresa',blank=True, null=True)
    link = models.URLField(max_length=200,blank=True, null=True)
    activo = models.BooleanField(default=True)    
    
    def __str__(self) -> str:
        return self.nombre
    
class AsesorEmpresa(models.Model):
    asesor = models.ForeignKey('Asesor', on_delete=models.CASCADE)
    empresa = models.ForeignKey('EmpresaContratante', on_delete=models.CASCADE)
    correo_empleado = models.EmailField(max_length=254)
    codigo_empleado = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20,blank=True, null=True,default=None)

    def __str__(self) -> str:
        return f"{self.asesor} - {self.empresa}"
    
    class Meta:
        unique_together = (("codigo_empleado", "empresa"),)

class Asesor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    empresa = models.ManyToManyField(EmpresaContratante, through=AsesorEmpresa)

    def __str__(self) -> str:
        return f"{self.usuario.first_name} {self.usuario.last_name}"

    

class Planes(models.Model):
    clave = ClaveField()
    nombre = models.CharField(max_length=100, blank=True, null=True)
    empresa = models.ForeignKey(EmpresaContratante, on_delete=models.CASCADE)
    gastos_medicos = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    
    
    def __str__(self) -> str:
        return self.nombre

class PersonaBase(models.Model):
    curp = ClaveField()
    tipo_persona = models.ForeignKey(TipoPersona, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=80)  # Asegúrate de que el max_length sea suficiente para ambos casos
    primer_apellido = models.CharField(max_length=120)
    segundo_apellido = models.CharField(max_length=120, blank=True, null=True)
    genero = models.CharField(max_length=1, choices=OPCIONES_GENERO)
    estatus_persona = models.CharField(max_length=10, choices=STATUS_PERSONA) ## Hay catalogo de estatus de personas?    

    class Meta:
        abstract = True

class PersonaPrincipal(PersonaBase):  
    asesor_cliente = models.ForeignKey(Asesor, on_delete=models.CASCADE)
    lugar_nacimiento = models.CharField( max_length=50, blank=True, null=True)  
    fecha_nacimiento = models.DateField()   
    #direccion
    asentamiento = models.ForeignKey(sepomex.Asentamiento, on_delete=models.CASCADE, null=True, default=None)
    calle = models.CharField(max_length=100,blank=True, null=True, default=None)
    numero = models.CharField(max_length=5,blank=True, null=True, default=None)
    numero_interior = models.CharField(max_length=100,blank=True, null=True, default=None)
    correo = models.EmailField( blank=True, null=True, default="correo@empresa.com")
    telefono = models.CharField(max_length=100, blank=True, null=True, default=None)
    

class PersonaRelacionada(PersonaBase):
    #Nombre, parentesco, porcentaje
    parentesco = models.ForeignKey(Parentesco, on_delete=models.CASCADE)
    persona_principal = models.ForeignKey(PersonaPrincipal, on_delete=models.CASCADE) 
    

class Poliza(models.Model):
    empresa = models.ForeignKey(EmpresaContratante, on_delete=models.CASCADE)
    asesor_poliza = models.ForeignKey(Asesor, on_delete=models.CASCADE) ## usuario
    numero_poliza = models.CharField(max_length=25)  
    persona_principal =  models.ForeignKey(PersonaPrincipal, on_delete=models.CASCADE) 
    forma_pago = models.ForeignKey(FormaPago, on_delete=models.CASCADE)  
    tipo_conducto_pago = models.ForeignKey(TipoConductoPago, on_delete=models.CASCADE) 
    plan = models.ForeignKey(Planes, on_delete=models.CASCADE)    
    fecha_vigencia = models.DateField()  
    fecha_emision = models.DateField(blank=True, null=True, default=None)
    fecha_pago = models.DateField(blank=True, null=True, default=None)
    estatus = models.CharField( max_length=10, choices=STATUS_GASTOS_MEDICOS)  ## Hay catalogo de estatus de polizas?

    class Meta:
        unique_together = (("empresa", "numero_poliza"),)
    

class Beneficiarios(models.Model):
    numero_poliza = models.ForeignKey(Poliza, on_delete=models.CASCADE)  
    parentesco = models.ForeignKey(Parentesco, on_delete=models.CASCADE,blank=True, null=True,default=None) 
    nombre_completo = models.CharField(max_length=100)  
    porcentaje_participacion = models.PositiveSmallIntegerField(default=0)  
    
    class Meta:
        unique_together = (("numero_poliza", "parentesco"),)
    

class CheckDocumentos(models.Model):
    numero_poliza = models.ForeignKey(Poliza, on_delete=models.CASCADE)  
    plan = models.ForeignKey(Planes, on_delete=models.CASCADE)
    empresa = models.ForeignKey(EmpresaContratante, on_delete=models.CASCADE)
    documento = models.ForeignKey(Documentos,on_delete=models.CASCADE)
    necesario = models.CharField(max_length=1,choices=OPCIONES_BOLEANO)
    entregado = models.CharField(max_length=1,choices=OPCIONES_BOLEANO)
    archivo = models.FileField()
    fecha_adjuntado = models.DateTimeField()      


class PlanDocumentos(models.Model):
    empresa = models.ForeignKey(EmpresaContratante, on_delete=models.CASCADE)
    documento = models.ForeignKey(Documentos, on_delete=models.CASCADE)
    

class Siniestros(models.Model):
    poliza = models.ForeignKey(Poliza,on_delete=models.CASCADE)
    numero_siniestro = models.PositiveSmallIntegerField( blank=True, null=True)  
    descripcion_siniestro = models.CharField(max_length=500, blank=True, null=True)  
    fecha_evento = models.DateTimeField()  
    estatus = models.CharField(max_length=10)
    

