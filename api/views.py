import json
import pprint
from django.utils import timezone 
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.shortcuts import render, redirect
from .serializers import UserRegistrationSerializer, PedidoSerializer
from .models import Pedido
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
        # Procesar el JSON recibido
        try:
            # Cargar el JSON desde el body de la petición
            data = json.loads(request.body)

            # Obtener cliente_id, por ejemplo, del usuario autenticado
            id_cliente = request.user if request.user.is_authenticated else 'User Test'

            # Obtener la fecha actual
            date_now = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

            # Guarda en la base de datos
            pedido = Pedido(cliente=id_cliente, fecha=date_now, data=data)
            pedido.save()

            return JsonResponse({'success': True, 'data': data}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

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
    def get(self, request):
        today = timezone.now().date() 
        pedidos = Pedido.objects.filter(fecha__date=today)
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)
        