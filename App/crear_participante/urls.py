from django.urls import path
from App.crear_participante import views

urlpatterns = [
    path('', views.crear_participante, name="crear_participante"),
    path('existe_participante/<str:rut_cliente>', views.busqueda_participante, name="existe_participante"),
    path('existe_usuario/<str:usuario>', views.busqueda_usuario, name="existe_usuario"),
    path('guardar_participante/', views.guardar_participante, name="guardar_participante"),
]
