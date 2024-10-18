# views.py
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from tema import models as tema_models
from documentos import models as doc_models
from sepomex import models as sepo_models

class SubscriptionAPIView(APIView):
    def post(self, request):
        serializer = serializers.SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SuscripcionViewSet(viewsets.ModelViewSet):
    queryset = tema_models.Subscription.objects.all()
    serializer_class =  serializers.SubscriptionSerializer

class AsesoresViewSet(viewsets.ModelViewSet):
    queryset = doc_models.Asesor.objects.all()
    serializer_class = serializers.AsesorSerializer

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = doc_models.EmpresaContratante.objects.all()
    serializer_class = serializers.EmpresaSerializer

class PolizasViewSet(viewsets.ModelViewSet):
    queryset = doc_models.Poliza.objects.all()
    serializer_class = serializers.PolizaSerializer

class ClientesViewSet(viewsets.ModelViewSet):
    queryset = doc_models.PersonaPrincipal.objects.all()
    serializer_class = serializers.ClienteSerializer

class AsentamientosViewSet(viewsets.ModelViewSet):
    queryset = sepo_models.Asentamiento.objects.all()
    serializer_class = serializers.AsentamientoSerializer

class CreaAsesorView(viewsets.ViewSet):
    def list(self, request):
        # Obtener todos los perfiles y suscripciones
        asesores = doc_models.Asesor.objects.all()
        suscripciones = tema_models.Suscripcion.objects.all()

        # Combinar los datos en una lista de diccionarios
        data = [
            {
                'asesor': asesor,
                'suscripcion': suscripciones.filter(usuario=asesores.usuario).first()
            }
            for asesor in asesores
        ]

        # Serializar los datos combinados
        serializer = serializers.CreaAsesorSerializer(data, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        # Obtener el Perfil por el ID
        try:
            perfil = Perfil.objects.get(pk=pk)
        except Perfil.DoesNotExist:
            return Response({"detail": "Perfil no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener la Suscripción asociada al usuario del Perfil
        suscripcion = Suscripcion.objects.filter(usuario=perfil.usuario).first()

        # Serializar el objeto combinado
        serializer = PerfilSuscripcionSerializer({'perfil': perfil, 'suscripcion': suscripcion})
        return Response(serializer.data)

    def create(self, request):
        # Crear un nuevo Perfil y Suscripción
        serializer = PerfilSuscripcionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        # Actualizar el Perfil y la Suscripción
        try:
            perfil = Perfil.objects.get(pk=pk)
        except Perfil.DoesNotExist:
            return Response({"detail": "Perfil no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        suscripcion = Suscripcion.objects.filter(usuario=perfil.usuario).first()

        # Serializar los datos combinados y actualizar
        serializer = PerfilSuscripcionSerializer(
            instance={'perfil': perfil, 'suscripcion': suscripcion},
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        # Eliminar el Perfil y la Suscripción asociada
        try:
            perfil = Perfil.objects.get(pk=pk)
            suscripcion = Suscripcion.objects.filter(usuario=perfil.usuario).first()

            # Eliminar ambos objetos
            perfil.delete()
            if suscripcion:
                suscripcion.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Perfil.DoesNotExist:
            return Response({"detail": "Perfil no encontrado."}, status=status.HTTP_404_NOT_FOUND)