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
]
