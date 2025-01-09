from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib import messages
from App.inicial.models import correo
from django.views.decorators.csrf import csrf_exempt

@login_required
def index(request):
    assert isinstance(request, HttpRequest)

    return render(request, 'correo/correo.html')

#Funcion de guardado de correo nuevo
@csrf_exempt
def guardar_correo(request):
    if request.method == 'POST':
        # Obtiene los datos del formulario POST
        nombre = request.POST.get('nombre')
        rut = request.POST.get('rut')
        correo_direccion = request.POST.get('correo')

        # Crea una nueva instancia del modelo 'correo' con los datos recibidos
        nuevo_correo = correo(
            nombre=nombre,
            rut=rut,
            correo=correo_direccion,
            valido=True
        )
        # Guarda el nuevo correo en la base de datos
        nuevo_correo.save()
        # Añade un mensaje de éxito a la lista de mensajes
        messages.success(request, 'Correo creado exitosamente')
    else:
        # Si la petición no es de tipo POST, añade un mensaje de error
        messages.error(request, 'Método no permitido')
    # Redirecciona al usuario de vuelta a la página de inicio (suponiendo que 'index' es la URL de la página de inicio)
    return redirect('index')

# Filtro utilizados para hacer busqueda en ajax,con javascript
def busqueda_rut(request,rut):
    # Filtra los datos del cliente por el rut proporcionado y que estén marcados como válidos
    datos_cliente = correo.objects.filter(rut=rut, valido=True)
    # Convierte los datos del queryset a una lista de diccionarios
    datacli = list(datos_cliente.values())
    # Devuelve los datos en formato JSON
    return JsonResponse(datacli, safe=False)

# Filtro utilizados para hacer busqueda en ajax,con javascript
def busqueda_correo(request,correo_ejecutivo):
    # Filtra los datos del cliente por el correo electrónico proporcionado y que estén marcados como válidos
    datos_cliente = correo.objects.filter(correo=correo_ejecutivo, valido=True)
    # Convierte los datos del queryset a una lista de diccionarios
    datacli = list(datos_cliente.values())
    # Devuelve los datos en formato JSON
    return JsonResponse(datacli, safe=False)