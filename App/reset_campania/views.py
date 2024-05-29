# Desarrollado por Manuel Godoy
from datetime import datetime

import pytz
from django.contrib import messages
from django.db import models
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.utils.timezone import make_aware
from django.utils import timezone
from App.inicial.models import campana, puntaje, historial_puntaje


# Create your views here.
def campania_actual(request):
    #Buscamos si existe una campaña activa
    campania_activa = campana.objects.filter(activo=True)

    if campania_activa.exists():
        #Retornamos el estado de la campaña activa como un JSON
        return JsonResponse({'campania_activa': True})
    return JsonResponse({'campania_activa': False})

def vista_reset(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'reset_campania/reset_campania.html',
        {
            'title':'reset campania Page',
        }
    )

def validacion_campania(request ,fecha_inicio, fecha_termino, hora_inicio, hora_termino):
    try:
        # Combinar fecha y hora en objetos datetime "naive"
        fecha_inicio_completa = datetime.strptime(f"{fecha_inicio} {hora_inicio}", "%Y-%m-%d %H:%M")
        fecha_termino_completa = datetime.strptime(f"{fecha_termino} {hora_termino}", "%Y-%m-%d %H:%M")

        # Convertir a objetos datetime "aware"
        zonaH = pytz.timezone('America/Santiago')  # Reemplaza 'America/Santiago' con tu zona horaria
        fecha_inicio_aware = make_aware(fecha_inicio_completa, zonaH)
        fecha_termino_aware = make_aware(fecha_termino_completa, zonaH)
    except ValueError:
        return JsonResponse({"error": "Formato de fecha no válido. Utilice el formato YYYY-MM-DDTHH:MM:SS."},
                            status=400)

        # Consulta para verificar si hay alguna campaña con un rango de fechas que se superponga
    campanas_superpuestas = campana.objects.filter(
        (models.Q(fecha_inicio__lte=fecha_inicio_aware) & models.Q(fecha_final__gte=fecha_inicio_aware)) |
        (models.Q(fecha_inicio__lte=fecha_termino_aware) & models.Q(fecha_final__gte=fecha_termino_aware)) |
        (models.Q(fecha_inicio__gte=fecha_inicio_aware) & models.Q(fecha_final__lte=fecha_termino_aware))
    )

    if campanas_superpuestas.exists():
        return JsonResponse({'permitir': False})

    return JsonResponse({'permitir': True})



def guardar_campania(activo,nombre_campania,fecha_inicio_aware,fecha_termino_aware):
    if activo != None:
        datos_campania = campana(
            nombre=nombre_campania,
            fecha_inicio=fecha_inicio_aware,
            fecha_final=fecha_termino_aware,
            activo=True
        )
        datos_campania.save()
    else:
        datos_campania = campana(
            nombre=nombre_campania,
            fecha_inicio=fecha_inicio_aware,
            fecha_final=fecha_termino_aware,
            activo=False
        )
        datos_campania.save()

def guardar_historial_puntaje(puntajes_actuales):
    for puntajes_actual in puntajes_actuales:
        historial_puntaje.objects.create(
            rut_ejecutivo=puntajes_actual.rut_ejecutivo,
            fecha_inicio_camp=puntajes_actual.fecha_inicio_camp,
            fecha_termino_camp=puntajes_actual.fecha_termino_camp,
            puntaje_periodo=puntajes_actual.puntaje_periodo,
            campania = puntajes_actual.campania_id
        )

def reset_puntajes(id_campania, fecha_inicio_aware, fecha_termino_aware):
    puntaje.objects.all().update(
        puntaje_periodo=0,
        fecha_inicio_camp=fecha_inicio_aware,
        fecha_termino_camp=fecha_termino_aware,
        fecha_reset=timezone.now(),
        fecha_movimiento=timezone.now(),
        campania_id=id_campania
    )

def reset_campania(request):
    # Verificación del método HTTP
    if request.method == 'POST':
        try:
            #Obtención de datos del formulario
            nombre_campania = request.POST.get("nombre_campania")
            fecha_inicio = request.POST.get("fecha_inicio")
            fecha_termino = request.POST.get("fecha_termino")
            hora_inicio = request.POST.get("hora_inicio")
            hora_termino = request.POST.get("hora_termino")
            activo = request.POST.get("activo")

            # Combinar fecha y hora en objetos datetime "naive"
            fecha_inicio_completa = datetime.strptime(f"{fecha_inicio} {hora_inicio}", "%Y-%m-%d %H:%M")
            fecha_termino_completa = datetime.strptime(f"{fecha_termino} {hora_termino}", "%Y-%m-%d %H:%M")

            # Convertir a objetos datetime "aware"
            zonaH = pytz.timezone('America/Santiago')  # Reemplaza 'America/Santiago' con tu zona horaria
            fecha_inicio_aware = make_aware(fecha_inicio_completa, zonaH)
            fecha_termino_aware = make_aware(fecha_termino_completa, zonaH)

            if activo != None:
                #Desactivar la campaña actual
                campania_actual = campana.objects.filter(activo=True)
                if campania_actual.exists():
                    campania_actual_activa = campana.objects.get(activo=True)
                    campania_actual_activa.activo = False
                    campania_actual_activa.save()

                #Crear nueva campaña
                guardar_campania(activo,nombre_campania,fecha_inicio_aware,fecha_termino_aware)

                #contamos los registros en la tabla de puntajes
                num_tabla_puntaje = puntaje.objects.all().count()

                if num_tabla_puntaje > 0:
                    #Obtenemos todos los puntajes actuales
                    puntajes_actuales = puntaje.objects.all()

                    #Guardamos los puntajes actuales en el historial de puntajes
                    guardar_historial_puntaje(puntajes_actuales)

                    #Reseteamos los valores de la tabla puntajes y actualizamos las fechas
                    campania_actual_guardada = campana.objects.get(activo = True)
                    id_campania = campania_actual_guardada.id
                    reset_puntajes(id_campania ,fecha_inicio_aware, fecha_termino_aware)


                    messages.success(request, "Se reseteo la campaña exitosamente..")
                else:
                    messages.error(request, "La tabla puntaje no posee registros..")

            else:
                # Crear nueva campaña
                guardar_campania(activo, nombre_campania, fecha_inicio_aware, fecha_termino_aware)


                messages.success(request, "Se guardo la campaña exitosamente..")


        except Exception as e:
            #Manejamos las excepciones
            messages.error(request, f'Ocurrió un error: {str(e)}')
            return redirect('reset')
    return redirect('reset')