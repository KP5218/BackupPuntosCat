from django.urls import path
from App.premio import views

urlpatterns = [
    path('', views.premio, name="premio"),
    path('agregar_premio/', views.agregar_premio, name="agregar_premio"),
    path('buscar_campana/', views.buscar_campana, name="buscar_campana"),
]
