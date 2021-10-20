from re import S
from Users.models import CustomUser
from rest_framework import serializers
from .models import Wallet, MerchantOuter, Service, ServiceTransaction, MoneyTransfer
import random
class ServiceSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Service
        fields = ('id', 'name', 'description', 'cost', 'currency', 'create_datetime', 'modify_datetime')
    
    def create(self, validated_data):
        return Service.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name        = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.cost        = validated_data.get('cost', instance.cost)
        instance.currency    = validated_data.get('currency', instance.currency)
        instance.save()
        return instance

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('id', 'number_wallet', 'balance', 'user',  'create_datetime', 'modify_datetime')
    
    def create(self, validated_data):
        #validated_data['number_wallet'] = str(random.randint(100, 10000000000000000000))
        return Wallet.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.balance = validated_data.get('balance', instance.balance)
        instance.save()
        return instance

