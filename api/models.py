from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    nombre = models.CharField(max_length=150)
    ROL_CHOICES = [
        ('depositos_globales', 'Depósitos Globales'),
        ('depositos_proveedores', 'Depósitos Proveedores'),
    ]
    rol = models.CharField(max_length=50, choices=ROL_CHOICES)

    def __str__(self):
        return self.username
class Pedido(models.Model):
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Relación con el usuario
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha del pedido
    material = models.CharField(max_length=100)  # Nombre del material
    cantidad = models.PositiveIntegerField()  # Cantidad del material
class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('entregada', 'Entregada'),
    ]
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)  # Relación con el pedido
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Relación con el cliente (usuario)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='pendiente')  # Estado de la reserva

