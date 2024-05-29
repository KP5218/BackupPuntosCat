from django.contrib import admin

from App.inicial.models import puntaje, correo, servicios, cargos

# Register your models here.
admin.site.register(puntaje)
admin.site.register(correo)
admin.site.register(servicios)
admin.site.register(cargos)