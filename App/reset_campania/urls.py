#Desarrollado por Manuel Godoy
from django.urls import path
from App.reset_campania import views

urlpatterns = [
    path('', views.vista_reset, name = "reset"),
    path('reset_campania/', views.reset_campania, name = "reset_campania"),
    path('campania_activa/', views.campania_actual, name = "campania_activa"),
    path('validacion_campania/<str:fecha_inicio>/<str:fecha_termino>/<str:hora_inicio>/<str:hora_termino>/', views.validacion_campania, name="validacion_campania")
]
