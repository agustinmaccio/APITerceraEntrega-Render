from django.urls import path
from . import views

urlpatterns = [
    path('login/',          views.UserLoginView.as_view(),  name='user_login'),
    path('home/',           views.home,                     name='home'),
    path('',                views.home,                     name='home'),
    path('CRC/',            views.CRC,                      name='CRC'),    
    path('carga_pedidos/',  views.carga_pedidos,            name='carga_pedidos'),
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('listPedidos/', views.PedidosAPIView.as_view(), name='list-pedidos'),
    path('listPedidos/<str:fecha>/', views.PedidosAPIView.as_view(), name='list-pedidos-fecha'),
    path('reservas/', views.UserReservasView.as_view(), name='user_reservas'),
    path('reservas/crear/', views.UserReservaCreateView.as_view(), name='user_reserva_create'),
]
