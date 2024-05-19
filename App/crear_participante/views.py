from datetime import date

from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from App.inicial.models import puntaje, campana


# Create your views here.
def crear_participante(request):

    return render(
        request,
        'app/crear_participante.html',
    )

def busqueda_participante(request,rut_cliente):
    datos_cliente = puntaje.objects.filter(rut_ejecutivo=rut_cliente, anulado=False)
    datacli = list(datos_cliente.values())
    return JsonResponse(datacli, safe=False)

def busqueda_usuario(request,usuario):
    datos_cliente = puntaje.objects.filter(user_ejecutivo=usuario, anulado=False)
    datacli = list(datos_cliente.values())
    return JsonResponse(datacli, safe=False)


def guardar_participante(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        usuario = request.POST.get('usuario')
        n_personal = request.POST.get('n_personal')
        nombre = request.POST.get('nombre')
        hoy = date.today()

        existe_rut = puntaje.objects.filter(rut_ejecutivo=rut)
        existe_usuario = puntaje.objects.filter(user_ejecutivo=usuario)

        if existe_usuario or existe_rut:
            messages.error(request, 'Este usuario ya existe en base de datos.')
            return redirect('crear_participante')

        campania_actual = campana.objects.filter(activo=True).last()
        if campania_actual:
            fecha_inicio = campania_actual.fecha_inicio
            fecha_final = campania_actual.fecha_final

            participante = puntaje(rut_ejecutivo=rut, user_ejecutivo=usuario, n_personal=n_personal, nombre_ejecutivo=nombre,fecha_inicio_camp=fecha_inicio,fecha_termino_camp=fecha_final,fecha_inicio_sistema=hoy)
            participante.save()
        else:
            participante = puntaje(rut_ejecutivo=rut, user_ejecutivo=usuario, n_personal=n_personal,
                                   nombre_ejecutivo=nombre, fecha_inicio_sistema=hoy)
            participante.save()

        messages.success(request, 'El participante se añadió con exito.')
        return redirect('crear_participante')


    return redirect('crear_participante')