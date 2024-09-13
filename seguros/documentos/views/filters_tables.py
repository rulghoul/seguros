import django_tables2 as tables
from django_filters import FilterSet

from documentos import models as mod

CONFIGURACION_TABLA = {"class": "table table-striped table-sm table-bordered",
                 "thead":{"class":"table-dark"},
                }  

class PolizaFilter(FilterSet):
    class Meta:
        model = mod.Poliza
        fields = {"estatus": ["exact"], "numero_poliza": ["exact"]}

class PolizaTable(tables.Table):
    telefono = tables.Column(accessor="persona_principal__telefono",)
    persona_principal = tables.Column(verbose_name="Nombre de Cliente", orderable=False)
    empresa = tables.Column(verbose_name="Aseguradora")
    acciones = tables.TemplateColumn(template_name='tabla/acciones.html', orderable=False)
    fecha_pago = tables.Column(localize=True)
    fecha_emision = tables.Column(localize=True)
    class Meta:
        model = mod.Poliza
        #template_name = "django_tables2/bootstrap5-responsive.html"
        sequence = ("persona_principal", 
                    "telefono", 
                    "empresa", 
                    "plan", 
                    "numero_poliza", "forma_pago", "fecha_pago", 
                    "fecha_emision", "estatus", "acciones" )
        exclude = ("asesor_poliza", "id", "monto_pago", 
                   "suma_asegurada", "unidad_pago",
                   "renovacion", "periodo",
                   "tipo_conducto_pago", "fecha_vigencia",)
        attrs = CONFIGURACION_TABLA   