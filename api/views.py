import json
import pprint
from django.utils import timezone 
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime 
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.shortcuts import render, redirect
from .serializers import UserRegistrationSerializer, PedidoSerializer, ReservaSerializer
from .models import Pedido, Reserva
from .permissions import IsDepositosGlobales, IsDepositosProveedores


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Autenticar al usuario usando el modelo de usuario por defecto
        user = authenticate(username=username, password=password)

        if user is not None:
            # Generar tokens JWT
            access = AccessToken.for_user(user)
            refresh = RefreshToken.for_user(user)   

            return Response({
                "refresh": str(refresh),
                "access": str(access),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

def home(request):
    # Si el usuario no es un depósito, simplemente renderizar la página
    return render(request, 'home.html')


def CRC(request):
    # Lógica para la página de inicio de sesión
    return render(request, 'CRC.html')


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  
def carga_pedidos(request):
    if request.method == 'POST':
        # Asigna el cliente al usuario autenticado
        cliente = request.user
        
        # Obtiene los datos del pedido enviados en la solicitud
        data = request.data
        data['cliente'] = cliente.id  # Asigna el ID del cliente al campo cliente

        # Crea el pedido con el usuario autenticado como cliente
        serializer = PedidoSerializer(data=data)

        if serializer.is_valid():
            # Si los datos son válidos, guarda el nuevo pedido y asigna el cliente
            pedido = serializer.save(cliente=cliente)
            return Response({
                "success": "Pedido creado con éxito.",
                "data": PedidoSerializer(pedido).data
            }, status=status.HTTP_201_CREATED)
        else:
            # Si los datos no son válidos, retorna los errores
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return render(request, 'carga_pedidos.html')
        
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Guarda el nuevo usuario
            return Response({"message": "Usuario registrado con éxito"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PedidosAPIView(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request, fecha=None):  # `fecha` ahora viene de la URL
        if fecha:
            try:
                # Convierte el parámetro `fecha` usando el formato `YYYY-MM-DD`
                fecha_obj = datetime.strptime(fecha, '%d-%m-%Y').date()
            except ValueError:
                return Response({'error': 'Fecha no válida. Use el formato YYYY-MM-DD.'}, status=400)
        else:
            # Si no se proporciona fecha, usa la fecha de hoy
            fecha_obj = timezone.now().date()

        # Filtra los pedidos por la fecha resultante
        pedidos = Pedido.objects.filter(fecha__date=fecha_obj)
        pedidos = pedidos.filter(reserva__isnull=True)
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)
        
class UserReservasView(APIView):
    """
    Vista para listar las reservas del usuario autenticado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Obtiene el usuario autenticado
        user = request.user

        # Filtra las reservas asociadas al usuario autenticado
        reservas = Reserva.objects.filter(cliente=user)

        # Serializa los datos
        serializer = ReservaSerializer(reservas, many=True)

        # Devuelve la respuesta con las reservas del usuario
        return Response(serializer.data, status=status.HTTP_200_OK)
class UserReservaCreateView(APIView):
    """
    Vista para crear una reserva para el usuario autenticado.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Obtiene el usuario autenticado
        user = request.user

        # Obtiene los datos de la reserva desde el cuerpo de la solicitud
        data = request.data
        
        # Asigna el cliente al usuario autenticado (esto puede ser un ForeignKey en tu modelo Reserva)
        data['cliente_id'] = user.id  # Asegura que el cliente es el usuario autenticado

        # Crea un serializer con los datos recibidos
        serializer = ReservaSerializer(data=data)

        # Verifica si los datos son válidos
        if serializer.is_valid():
            # Guarda la reserva en la base de datos
            reserva = serializer.save(cliente=user)

            # Devuelve la respuesta con los datos de la reserva creada
            return Response({
                'success': True,
                'data': ReservaSerializer(reserva).data
            }, status=status.HTTP_201_CREATED)
        
        # Si los datos no son válidos, retorna los errores
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)