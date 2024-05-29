#Desarrolado por Barbara Vera
from datetime import date
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from App.inicial.models import puntaje, campana, servicios, cargos


# Create your views here.
def crear_participante(request):
    opciones_servicios = servicios.objects.all()
    opciones_cargos = cargos.objects.all()
    return render(
        request,
        'app/crear_participante.html',{
            'opciones_servicios':opciones_servicios,
            'opciones_cargos':opciones_cargos
        }
    )

def busqueda_participante(request,rut_cliente):
    #filtro de participantes por rut
    datos_cliente = puntaje.objects.filter(rut_ejecutivo=rut_cliente, anulado=False)
    datacli = list(datos_cliente.values())
    return JsonResponse(datacli, safe=False)

def busqueda_usuario(request,usuario):
    #busqueda de partipitante por usuario
    datos_cliente = puntaje.objects.filter(user_ejecutivo=usuario, anulado=False)
    datacli = list(datos_cliente.values())
    return JsonResponse(datacli, safe=False)


def guardar_participante(request):
    # Verifica si el método de la solicitud es POST
    if request.method == 'POST':
        # Obtiene los datos enviados por el formulario
        rut = request.POST.get('rut')
        usuario = request.POST.get('usuario')
        #n_personal = request.POST.get('n_personal')
        nombre = request.POST.get('nombre')
        cargo = request.POST.get('cargo')
        servicio = request.POST.get('servicio')
        hoy = date.today()

        # Verifica si ya existe un participante con el rut o usuario proporcionado
        existe_rut = puntaje.objects.filter(rut_ejecutivo=rut)
        existe_usuario = puntaje.objects.filter(user_ejecutivo=usuario)

        if existe_usuario or existe_rut:
            # Si ya existe, muestra un mensaje de error y redirige a la página de creación de participante
            messages.error(request, 'Este usuario ya existe en base de datos.')
            return redirect('crear_participante')

        obj_cargo = cargos.objects.get(cod_cargo=cargo)
        obj_servicio = servicios.objects.get(cod_servicio=servicio)
        # Obtiene la última campaña activa (si existe alguna)
        campania_actual = campana.objects.filter(activo=True).last()

        if campania_actual:
            # Si hay una campaña activa, obtiene sus fechas de inicio y final
            fecha_inicio = campania_actual.fecha_inicio
            fecha_final = campania_actual.fecha_final

            # Crea un nuevo participante con las fechas de la campaña
            participante = puntaje(rut_ejecutivo=rut, user_ejecutivo=usuario, nombre_ejecutivo=nombre,
                                   fecha_inicio_camp=fecha_inicio,fecha_termino_camp=fecha_final,fecha_inicio_sistema=hoy,cod_cargo=obj_cargo, cod_servicio=obj_servicio,campania_id=campania_actual)
            participante.save()
        else:
            # Si no hay una campaña activa, crea un nuevo participante sin fechas de campaña
            participante = puntaje(rut_ejecutivo=rut, user_ejecutivo=usuario,nombre_ejecutivo=nombre, fecha_inicio_sistema=hoy,cod_cargo=obj_cargo, cod_servicio=obj_servicio)
            participante.save()
        # Muestra un mensaje de éxito y redirige a la página de creación de participante
        messages.success(request, 'El participante se añadió con exito.')
        return redirect('crear_participante')

    # Si el método no es POST, redirige a la página de creación de participante
    return redirect('crear_participante')