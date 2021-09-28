from types import prepare_class
from WalletController.serializers import ServiceSerializer
from WalletController.models import Service
from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

#from apps.services.permissions import AdminCreatOrUserRead
# Create your views here.
class ServiceView(APIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    #permission_classes = [AdminCreatOrUserRead]
    permission_classes = (permissions.AllowAny,)

    # POST - create new service. TODO: AllowedOnly to ADMIN
    def post(self, request):
        if request.method == 'POST':
            _service = {k:v[0] for k,v in dict(request.POST).items()}
            _service_serializer = ServiceSerializer(data=_service)
            if _service_serializer.is_valid():
                _service_serializer.save()
                return JsonResponse(_service_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(_service_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def get(self, request, pk=None):
        if request.method == 'GET':
            _services = Service.objects.all()
            _service_serializer = ServiceSerializer(_services, many=True)
        return JsonResponse(_service_serializer.data, safe=False)

