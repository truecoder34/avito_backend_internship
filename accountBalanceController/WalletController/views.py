from types import prepare_class
from WalletController.serializers import ServiceSerializer
from WalletController.models import Service
from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

'''
SERVICE VIEW CLASS
'''
class ServiceView(APIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    #permission_classes = [AdminCreatOrUserRead]
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    '''
        Method to handle requests POST 
        1) create new service.          - TODO: AllowedOnly to ADMIN
    '''
    def post(self, request):
        _service = {k:v[0] for k,v in dict(request.POST).items()}
        _service_serializer = ServiceSerializer(data=_service)
        if _service_serializer.is_valid():
            _service_serializer.save()
            return JsonResponse(_service_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(_service_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    '''
        Method to handle GET requests:
        1) get all service entites ; api/service/
        2) get service(s) by filter name ; api/service?name=test . Currently support only name. Need to extend 
        on description and currency
        3) get service by PK  ; api/service/<uuid:pk>
    '''
    def get(self, request, filter=None, pk=None):
        _service = Service.objects.all()
        
        if pk != None :
            try:
                _service = Service.objects.get(pk=pk)
                _service_serializer = ServiceSerializer(_service)
            except Service.DoesNotExist:
                return JsonResponse({'message': 'The service does not exist'}, status=status.HTTP_404_NOT_FOUND)
        elif len(request.query_params) != 0:
            _filter = request.query_params.dict()
            print('[DEBUG] : KEY ',  list(_filter)[0])
            print('[DEBUG] : Quey params ', request.query_params.dict())      # equal to dict(zip(request.GET.keys(), request.GET.values()))
            _filter = request.GET.get(list(_filter)[0], None)
            _service = _service.filter(name__icontains=_filter)
            _service_serializer = ServiceSerializer(_service, many=True)
        else:
            _service_serializer = ServiceSerializer(_service, many=True)

        return JsonResponse(_service_serializer.data, safe=False)

    '''
        Method to handle GET requests :
        1) delete all Services ; api/service/           - TODO: AllowedOnly to ADMIN
        2) delete Service by ID ; api/service/<uuid:pk> - TODO: AllowedOnly to ADMIN
    '''
    def delete(self, request,pk=None):
        if pk == None:
            count = Service.objects.all().delete()
            return JsonResponse({'message': '{} Services were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)
        else: 
            _service = Service.objects.get(pk=pk)
            _service.delete()
            return JsonResponse({'message': 'Application was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    '''
    Method to handle PUT requests :
    1) Update service by pk ; api/service/           - TODO: AllowedOnly to ADMIN
    '''
    def put(self, request, pk):
        # find application by pk (id)
        try:
            _service = Service.objects.get(pk=pk)
            _service_serializer = ServiceSerializer(_service)
        except Service.DoesNotExist:
            return JsonResponse({'message': 'The service does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        _service_updates = {k:v[0] for k,v in dict(request.POST).items()}
        print("[DEBUG] SERVICE DATA FROM PUT BODY" , _service_updates)

        _service_serializer = ServiceSerializer(_service, data=_service_updates)
        if _service_serializer.is_valid():
            _service_serializer.save()
            return JsonResponse(_service_serializer.data)

'''
WALLET VIEW CLASS
'''
