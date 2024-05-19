from django.urls import path
from App.inicial import views

urlpatterns = [
    path('', views.home, name="home"),
    path('home/', views.home, name="home"),
    path('mostrar_premio/', views.mostrar_premio, name="mostrar_premio"),
    path('insertar_derivacion/', views.insertar_derivacion, name="insertar_derivacion"),
    path('base_cliente/<str:rut_cliente>', views.filtrocliente, name="datos_base_cliente"),
    path('busqueda/<str:rut_cliente>', views.busqueda_cliente, name="busqueda"),

]
