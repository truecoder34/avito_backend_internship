from Users.models import CustomUser
from rest_framework import serializers
from .models import Wallet, MerchantOuter, Service, ServiceTransaction, MoneyTransfer

class ServiceSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Service
        fields = ('id', 'name', 'description', 'cost', 'currency')
