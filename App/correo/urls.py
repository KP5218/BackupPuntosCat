from django.urls import path
from App.correo import views

urlpatterns = [
    path('', views.index, name="index"),
    path('guardar_correo/',views.guardar_correo, name='guardar_correo'),
]
