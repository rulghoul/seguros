# serializers.py
from documentos.models import Asesor, AsesorEmpresa, EmpresaContratante
from documentos.utils.send_email_new_asesor import envia_correo_new_asesor as envia
from tema.models import Subscription
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

    def create(self, validated_data):
        user = User.objects.get(username=validated_data['username'])
        if not user:
            user = User.objects.create_user(**validated_data)
            request = self.context.get('request')
            envia(request, user)
        return user

class AsesorEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsesorEmpresa
        fields = ['empresa', 'correo_empleado', 'codigo_empleado', 'telefono']

class AsesorSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    empresas = AsesorEmpresaSerializer(many=True, source='asesorempresa_set')

    class Meta:
        model = Asesor
        fields = ['usuario', 'empresas']

    def create(self, validated_data):
        user_data = validated_data.pop('usuario')
        empresa_data = validated_data.pop('asesorempresa_set')
        user = User.objects.get(username=user_data['username'])
        if not user:
            user = User.objects.create_user(username=user_data['username'], email=user_data['email'], password=None)
            created = True

        # Crear Asesor
        asesor = Asesor.objects.create(usuario=self.usuario, **validated_data)

        if created:
            request = self.context.get('request')
            envia(request, user)
        # Crear AsesorEmpresa
        for empresa in empresa_data:
            empresa_object = EmpresaContratante.objects.get(nombre=empresa['empresa'])
            if empresa_object:
                AsesorEmpresa.objects.create(asesor=asesor, empresa=empresa_object, correo_empleado=empresa['correo_empleado'], codigo_empleado=empresa['codigo_empleado'], telefono=empresa['telefono'] )
        
        return asesor

class SubscriptionSerializer(serializers.ModelSerializer):
    asesor = AsesorSerializer()

    class Meta:
        model = Subscription
        fields = ['asesor', 'subscription_type', 'start_date']

    def create(self, validated_data):
        asesor_data = validated_data.pop('asesor')
        # Crear o actualizar el asesor y usuario asociado
        asesor = AsesorSerializer.create(AsesorSerializer(context=self.context), validated_data=asesor_data)
        user = asesor.usuario

        # Obtener o crear la suscripción vinculada al usuario
        subscription, created = Subscription.objects.get_or_create(user=user, subscription_type=validated_data['subscription_type'], start_date=validated_data['end_date'] )

        if not created:
            # Si la suscripción ya existe, actualiza el tipo y la fecha de finalización
            subscription.subscription_type = validated_data.get('subscription_type', subscription.subscription_type)
            subscription.save()

        return subscription
