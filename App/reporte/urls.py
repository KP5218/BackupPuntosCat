from django.urls import path
from App.reporte import views

urlpatterns = [
    path('', views.index, name="index"),
    path('fecha_derivacion/', views.fecha_derivacion, name='fecha_derivacion'),
    path('fecha_puntaje/', views.fecha_puntaje, name='fecha_puntaje'),
    path('fecha_campania/', views.fecha_campania, name='fecha_campania'),
    path('buscar_campana/', views.buscar_campana, name="buscar_campana"),
    path('campania_csv/', views.campania_csv, name="campania_csv"),
    path('csv_derivaciones/', views.csv_derivaciones, name="csv_derivaciones"),
    path('csv_puntaje/', views.csv_puntaje, name="csv_puntaje"),
    path('datos/', views.datos, name="datos"),
    path('buscar_detalles_campana/', views.buscar_detalles_campana, name='buscar_detalles_campana'),
    path('bcsv_datos_cliente/', views.csv_datos_cliente, name='csv_datos_cliente'),

]
