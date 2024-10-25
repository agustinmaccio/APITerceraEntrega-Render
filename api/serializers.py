from django.contrib.auth import get_user_model
from .models import Pedido
from rest_framework import serializers

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    rol = serializers.ChoiceField(choices=[
        ('depositos_globales', 'Depósitos Globales'),
        ('depositos_proveedores', 'Depósitos Proveedores')
    ], required=False)
    direccion = serializers.CharField(required=False, allow_blank=True)
    telefono = serializers.CharField(required=False, allow_blank=True)
    nombre = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'direccion', 'telefono', 'nombre', 'rol')

    def create(self, validated_data):
        # Crea un nuevo usuario usando el método create_user de Django
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            direccion=validated_data.get('direccion', ''),
            telefono=validated_data.get('telefono', ''),
            nombre=validated_data.get('nombre', ''),
            rol=validated_data.get('rol', '')
        )

        return user

    def validate_telefono(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("El teléfono debe contener solo dígitos.")
        return value

    def validate_nombre(self, value):
        if not value:
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value
    

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['fecha', 'data']  # O usa '__all__' si quieres todos los campos