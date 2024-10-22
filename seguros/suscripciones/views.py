# views.py
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from tema import models as tema_models
from documentos import models as doc_models
from sepomex import models as sepo_models
from django.contrib.auth.models import User
import json
from django.db import transaction

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

@transaction.atomic
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

class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class CreaAsesorView(viewsets.ViewSet):
    @transaction.atomic
    def list(self, request):
        # Obtener todos los perfiles y suscripciones
        asesores = doc_models.Asesor.objects.all()
        #suscripciones = tema_models.Subscription.objects.all()

        # Combinar los datos en una lista de diccionarios
        data = []
        for asesor in asesores:
            try:
                susc = tema_models.Subscription.objects.get(user=asesor.usuario)
            except tema_models.Subscription.DoesNotExist:
                susc = None
            data.append({'asesor': asesor,'suscripcion': susc})

        # Serializar los datos combinados
        serializer = serializers.CreaAsesorSuscripcionSerializer(data, many=True)

        return Response(serializer.data)

    @transaction.atomic
    def retrieve(self, request, pk=None):
        try:
            asesor = doc_models.Asesor.objects.get(pk=pk)
            try:
                suscripcion = tema_models.Subscription.objects.get(user=asesor.usuario)
            except tema_models.Subscription.DoesNotExist:
                suscripcion = None
            data = {'asesor': asesor, 'suscripcion': suscripcion}
            serializer = serializers.CreaAsesorSuscripcionSerializer(data)
            return Response(serializer.data)
        except doc_models.Asesor.DoesNotExist:
            return Response({"detail": "Asesor no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    def create(self, request):
        serializer = serializers.CreaAsesorSuscripcionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def update(self, request, pk=None):
        try:
            asesor = doc_models.Asesor.objects.get(pk=pk)
            try:
                suscripcion = tema_models.Subscription.objects.get(user=asesor.usuario)
            except tema_models.Subscription.DoesNotExist:
                suscripcion = None
            instance = {'asesor': asesor, 'suscripcion': suscripcion}
            serializer = serializers.CreaAsesorSuscripcionSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except doc_models.Asesor.DoesNotExist:
            return Response({"detail": "Asesor no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    def destroy(self, request, pk=None):
        try:
            asesor = doc_models.Asesor.objects.get(pk=pk)
            suscripcion = tema_models.Subscription.objects.filter(user=asesor.usuario).first()
            asesor.usuario.delete()  # Esto eliminará al usuario y, en cascada, al asesor si está configurado
            if suscripcion:
                suscripcion.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except doc_models.Asesor.DoesNotExist:
            return Response({"detail": "Asesor no encontrado."}, status=status.HTTP_404_NOT_FOUND)