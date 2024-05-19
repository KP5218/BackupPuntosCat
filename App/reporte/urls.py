from django.urls import path
from App.reporte import views

urlpatterns = [
    path('', views.index, name="index"),
    path('buscar-resultados/', views.buscar_resultados, name='buscar_resultados'),

]
