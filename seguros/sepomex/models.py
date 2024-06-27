from django.db import models

# SEPOMEX

class Estado(models.Model):
    clave = models.CharField(max_length=20, unique=True) #"c_estado"
    nombre = models.CharField(max_length=250, unique=True) #"d_estado"

    def __str__(self) -> str:
        return self.nombre

class Municipio(models.Model):    
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    clave = models.CharField(max_length=40,  default=None,null=True) #"c_mnpio"
    nombre = models.CharField(max_length=250) #"D_mnpio"

    def __str__(self) -> str:
        return self.nombre

class TipoAsentamiento(models.Model):
    clave = models.CharField(max_length=20,  default=None,null=True) #"d_tipo_asenta"
    nombre = models.CharField(max_length=250, unique=True) #"d_tipo_asenta"

    def __str__(self) -> str:
        return self.nombre

class Asentamiento(models.Model):
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    tipo_asentamiento = models.ForeignKey(TipoAsentamiento, on_delete=models.CASCADE)
    codigo_postal = models.CharField(max_length=5) #"d_CP"
    nombre = models.CharField(max_length=255)  #"d_asenta"

    class Meta:
            indexes = [
                models.Index(fields=["municipio", "nombre", "codigo_postal"], name="asentamiento_cp_idx"),
            ]

    def __str__(self) -> str:
        return f'{self.tipo_asentamiento}/{self.nombre}'

