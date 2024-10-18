# serializers.py
from documentos import models as doc_models
from tema.models import Subscription
from sepomex import models as sepo_models 
from django.contrib.auth.models import User
from documentos.utils.send_email_new_asesor import envia_correo_new_asesor as envia
from rest_framework import serializers
from rest_framework import viewsets

## SEPOMEX

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = sepo_models.Estado
        fields = ['nombre', ]

class MunicipioSerializer(serializers.ModelSerializer):
    estado = EstadoSerializer()
    class Meta:
        model = sepo_models.Municipio
        fields = ['estado', 'nombre', ]

class TipoAsentamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = sepo_models.TipoAsentamiento
        fields = ['nombre', ]

class AsentamientoSerializer(serializers.ModelSerializer):
    municipio = MunicipioSerializer()
    tipo_asentamiento = TipoAsentamientoSerializer()
    class Meta:
        model = sepo_models.Asentamiento
        fields = ['municipio', 'tipo_asentamiento', 'codigo_postal', 'nombre']



## TERMINA SEPOMEX

## Empieza Documentos 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def create(self, validated_data):
        user = User.objects.get(username=validated_data['username'])
        if not user:
            user = User.objects.create_user(**validated_data)
            request = self.context.get('request')
            envia(request, user)
        return user

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = doc_models.Asesor
        fields = ['nombre', 'empresa', 'gastosMedicos', 'activo']

class EmpresaSerializer(serializers.ModelSerializer):
    planes = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='planes_set')
    class Meta:
        model = doc_models.EmpresaContratante
        fields = ['clave', 'nombre', 'link', 'link_pago', 'activo', 'planes', ]


class AsesorEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = doc_models.AsesorEmpresa
        fields = ['empresa', 'correo_empleado', 'codigo_empleado', 'telefono']

class AsesorSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    empresas = AsesorEmpresaSerializer(many=True, source='asesorempresa_set')

    class Meta:
        model = doc_models.Asesor
        fields = ['usuario', 'empresas']

class ClienteSerializer(serializers.ModelSerializer):
    asesor_cliente = AsesorSerializer()
    asentamiento = AsentamientoSerializer()
    class Meta:
        model = doc_models.PersonaPrincipal
        fields = ['curp','nombre','primer_apellido','segundo_apellido','genero','estatus_persona',
                  'asesor_cliente','lugar_nacimiento','fecha_nacimiento',
                  'asentamiento','calle','numero','numero_interior',
                  'correo','telefono',]


class PolizaSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer()
    asesor_poliza = AsesorSerializer()
    class Meta:
        model = doc_models.Poliza
        fields = ['empresa', 'asesor_poliza', 'numero_poliza', 'persona_principal', 'forma_pago',
                  'tipo_conducto_pago', 'plan', 'fecha_vigencia', 'fecha_emision', 'fecha_pago',
                   'estatus',  'monto_pago', 'suma_asegurada', 'unidad_pago', 'renovacion', 'periodo' ]


class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer()    
    class Meta:
        model = Subscription
        fields = ['user', 'subscription_type', 'start_date', 'end_date'] 



class CreaAsesorSerializer(serializers.Serializer):
    asesor = AsesorSerializer()
    suscripcion = SubscriptionSerializer()

    def create(self, validated_data):
        # Extraer datos para cada modelo
        asesor_data = validated_data.get('asesor')
        suscripcion_data = validated_data.get('suscripcion')

        # Crear el objeto Perfil
        asesor = doc_models.Asesor.objects.create(**asesor_data)

        # Crear el objeto Suscripcion
        suscripcion = Subscription.objects.create(**suscripcion_data)

        # Retornar la combinación de ambos
        return {
            'perfil': asesor,
            'suscripcion': suscripcion
        }

    def update(self, instance, validated_data):
        # Actualizar datos del Perfil
        asesor_data = validated_data.get('asesor')
        suscripcion_data = validated_data.get('suscripcion')

        # Actualizar Perfil
        doc_models.Asesor.objects.filter(pk=instance['perfil'].pk).update(**asesor_data)

        # Actualizar Suscripcion
        Subscription.objects.filter(pk=instance['suscripcion'].pk).update(**suscripcion_data)

        # Recargar las instancias actualizadas
        instance['asesor'].refresh_from_db()
        instance['suscripcion'].refresh_from_db()

        return instance