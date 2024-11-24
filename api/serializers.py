from django.contrib.auth import get_user_model
from .models import CustomUser, Pedido, Reserva
from rest_framework import serializers

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    rol = serializers.ChoiceField(choices=[
        ('depositos_globales', 'Depósitos Globales'),
        ('depositos_proveedores', 'Depósitos Proveedores')
    ], required=True)
    direccion = serializers.CharField(required=False, allow_blank=True)
    telefono = serializers.CharField(required=False, allow_blank=True)
    nombre = serializers.CharField(required=True, allow_blank=True)

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
        fields = ['id', 'cliente', 'fecha', 'material', 'cantidad']  # Campos que quieres exponer

    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser un número positivo.")
        return value

    def validate_material(self, value):
        if not value:
            raise serializers.ValidationError("El material no puede estar vacío.")
        if len(value) > 100:
            raise serializers.ValidationError("El nombre del material no puede exceder los 100 caracteres.")
        return value
class ReservaSerializer(serializers.ModelSerializer):
    pedido_id = serializers.PrimaryKeyRelatedField(queryset=Pedido.objects.all(), source='pedido', write_only=True)
    cliente_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='cliente', write_only=True)
    pedido = PedidoSerializer(read_only=True)  # Opcional: Mostrar representación legible del pedido
    cliente = UserRegistrationSerializer(read_only=True)  # Opcional: Mostrar representación legible del cliente

    class Meta:
        model = Reserva
        fields = ['id', 'pedido_id', 'cliente_id', 'pedido', 'cliente', 'estado']
        read_only_fields = ['id', 'pedido', 'cliente']
    
    def validate(self, data):
        # Verifica si ya existe una reserva para el pedido en cuestión
        pedido = data.get('pedido')
        
        if Reserva.objects.filter(pedido=pedido).exists():
            raise serializers.ValidationError("Ya existe una reserva para este pedido.")
        
        return data