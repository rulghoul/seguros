from django.db import models

######################### Opciones ###########################

OPCIONES_GENERO = [
    ('H', 'Hombre'),
    ('M', 'Mujer'),
    ('O', 'Otro'),
    ]

OPCIONES_BOLEANO = [('S','Si'),('N',"No"),('I','Incompleto')]

######################### Catalogos ###########################

class TipoConductoPago(models.Model):
    clave = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    activo = models.IntegerField(default = True)

class TipoPersona(models.Model):
    clave = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)
    activo = models.IntegerField(default = True)

class FormaPago(models.Model):
    clave = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    activo = models.IntegerField(default = True)

class Documentos(models.Model):
    clave = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    activo = models.IntegerField(default = True)

class TipoMediocontacto(models.Model):
    descripcion = models.CharField(max_length=20)
    activo = models.IntegerField(default = True)

class Parentesco(models.Model):
    descripcion = models.CharField(max_length=20)
    activo = models.IntegerField(default = True)


######## Tablas Principales ############

class EmpresaContratante(models.Model):
    clave = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    activo = models.IntegerField(default = True)

class Planes(models.Model):
    clave = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    empresa = models.ForeignKey(EmpresaContratante, on_delete=models.CASCADE)
    activo = models.IntegerField(default = True)

class PersonaPrincipal(models.Model):
    clave = models.CharField(max_length=20)
    tipo_persona = models.ForeignKey(TipoPersona, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=20)
    primer_apellido = models.CharField( max_length=20)  
    segundo_apellido = models.CharField( max_length=20, blank=True, null=True)  
    lugar_nacimiento = models.CharField( max_length=50, blank=True, null=True)  
    feccha_nacimiento = models.DateTimeField()  
    genero = models.CharField(max_length=1,choices=OPCIONES_GENERO)
    estatus = models.CharField( max_length=10)  

class PersonaRelacionada(models.Model):
    id = models.SmallAutoField(primary_key=True)
    clave = models.CharField(max_length=20)
    tipo_persona = models.ForeignKey(TipoPersona, on_delete=models.CASCADE)
    persona_principal = models.ForeignKey(PersonaPrincipal, on_delete=models.CASCADE) 
    nombre = models.CharField(max_length=50)
    primer_apellido = models.CharField( max_length=50)  
    segundo_apellido = models.CharField( max_length=50, blank=True, null=True)  
    genero = models.CharField(max_length=1,choices=OPCIONES_GENERO)  
    estatus = models.CharField( max_length=10)  ## Hay catalogo de estatus de personas

class Poliza(models.Model):
    empresa = models.CharField(max_length=20)
    numero_poliza = models.PositiveSmallIntegerField()  
    persona_principal =  models.ForeignKey(PersonaPrincipal, on_delete=models.CASCADE) 
    forma_pago = models.ForeignKey(FormaPago, on_delete=models.CASCADE)  
    tipo_conducto_pago = models.ForeignKey(TipoConductoPago, on_delete=models.CASCADE) 
    plan = models.ForeignKey(Planes, on_delete=models.CASCADE)    
    fechavigencia = models.DateTimeField()  
    estatus = models.CharField( max_length=10)  

class Beneficiarios(models.Model):
    numero_poliza = models.PositiveSmallIntegerField()  
    persona_relacionada = models.ForeignKey(PersonaRelacionada, on_delete=models.CASCADE) 
    tipo_persona = models.ForeignKey(TipoPersona, on_delete=models.CASCADE) 
    #persona_principal = models.CharField( max_length=20)  
    porcentaje_participacion = models.PositiveSmallIntegerField( blank=True, null=True)  

class CheckDocumentos(models.Model):
    numero_poliza = models.PositiveSmallIntegerField()  
    plan = models.CharField(max_length=20)
    empresa = models.ForeignKey(EmpresaContratante, on_delete=models.CASCADE)
    documento = models.ForeignKey(Documentos,on_delete=models.CASCADE)
    necesario = models.CharField(max_length=1,choices=OPCIONES_BOLEANO)
    entregado = models.CharField(max_length=1,choices=OPCIONES_BOLEANO)
    archivo = models.FileField()
    fecha_adjuntado = models.DateTimeField()  


class PlanDocumentos(models.Model):
    clave = models.CharField(max_length=20)
    empresa = models.ForeignKey(EmpresaContratante, on_delete=models.CASCADE)
    documento = models.ForeignKey(Documentos, on_delete=models.CASCADE)

class Siniestros(models.Model):
    poliza = models.ForeignKey(Poliza,on_delete=models.CASCADE)
    numero_siniestro = models.PositiveSmallIntegerField( blank=True, null=True)  
    descripcion_siniestro = models.CharField( blank=True, null=True)  
    fecha_evento = models.DateTimeField()  
    estatus = models.CharField(max_length=10)

