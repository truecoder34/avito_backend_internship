from WalletController.models import Wallet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import CustomUser

class ExtendedTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(ExtendedTokenObtainPairSerializer, cls).get_token(user)
        # Add custom claim(s) which is phone 
        token['phone'] = user.phone
        return token

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the Meta class.
    """
    email       = serializers.EmailField(required=True)
    #username    = serializers.CharField()
    password    = serializers.CharField(min_length=8, write_only=True)
    phone       = serializers.CharField(max_length=10, help_text='Number without code, 10 symbols', label='Phone')
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'username', 'first_name', 'last_name', 'phone')
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate_first_name(self, value):
        if value == '':
            raise serializers.ValidationError('Specify your name...')
        return value

    def validate_last_name(self, value):
        if value == '':
            raise serializers.ValidationError('Specify your lastname...')
        return value

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Specify 10 numbers without region code. Ex.: 9998885544")
        if len(value) > 10:
            raise serializers.ValidationError('Too long phone number. Please double check it.')
        if len(value) < 10:
            raise serializers.ValidationError('Too short phone number. Please double check it.')
        phone = f'+7{value}'
        if CustomUser.objects.filter(phone=phone).exists():
            raise serializers.ValidationError(
                "User with this number already exists!")
        return value
    
    def validate_email(self, email_specified):
        if email_specified == '':
            raise serializers.ValidationError('Specify your email...')
        if CustomUser.objects.filter(email=email_specified).exists():
            raise serializers.ValidationError(
                "User with this email already exists!")
        return email_specified
    
    def validate_username(self, username_specified):
        if username_specified == '':
            raise serializers.ValidationError('Specify your username...')
        if CustomUser.objects.filter(username=username_specified).exists():
            raise serializers.ValidationError(
                "User with this username already exists!")
        return username_specified   
    
    

    # base Create method. 
    def create(self, validated_data):
        _phone = f"+7{validated_data['phone']}"
        user_instance = CustomUser(
                                    email=validated_data['email'],
                                    username=validated_data['username'],
                                    last_name=validated_data['last_name'],
                                    first_name=validated_data['first_name'],
                                    phone=_phone
        )
        password = validated_data.pop('password', None)
        #instance = self.Meta.model(**validated_data)  # as long as the fields are the same, we can just use this
        if password is not None:
            user_instance.set_password(password)
        user_instance.save()
        print("[DEBUG] : New user created {}".format(user_instance))
        # TODO : Create here instance of wallet for USER
        wallet = Wallet.objects.create(user=user_instance)
        wallet.save()
        return user_instance
    
    # TODO : add def upadate(self, instance, validated_data) method tu update users profile