from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from App.inicial.models import correo
from django.views.decorators.csrf import csrf_exempt

@login_required
def index(request):
    assert isinstance(request, HttpRequest)

    return render(request, 'correo/correo.html')

@csrf_exempt
def guardar_correo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        rut = request.POST.get('rut')
        correo_direccion = request.POST.get('correo')

        nuevo_correo = correo(
            nombre=nombre,
            rut=rut,
            correo=correo_direccion,
            valido=True
        )

        nuevo_correo.save()

        messages.success(request, 'Correo creado exitosamente')
    else:
        messages.error(request, 'Método no permitido')

    return redirect('index')