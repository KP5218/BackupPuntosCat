from django.urls import path
from App.correo import views

urlpatterns = [
    path('', views.index_correo, name="index_correo"),
    path('guardar_correo/',views.guardar_correo, name='guardar_correo'),
    path('existe_rut/<str:rut>',views.busqueda_rut, name='existe_rut'),
    path('existe_correo/<str:correo_ejecutivo>',views.busqueda_correo, name='existe_correo'),
]
