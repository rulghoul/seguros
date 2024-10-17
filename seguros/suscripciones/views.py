# views.py
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SubscriptionSerializer, AsesorEmpresaSerializer, AsesorSerializer
from tema.models import Subscription
from documentos.models import EmpresaContratante, AsesorEmpresa, Asesor

class SubscriptionAPIView(APIView):
    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SuscripcionViewSet(viewsets.ModelViewSet):
    queryset = Asesor.objects.all()
    serializer_class = AsesorSerializer