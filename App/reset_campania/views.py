from datetime import datetime

import pytz
from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.utils.timezone import make_aware
from django.utils import timezone
from App.inicial.models import campana, puntaje, historial_puntaje


# Create your views here.
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

def reset_campania(request):
    if request.method == 'POST':
        try:
            nombre_campania = request.POST.get("nombre_campania")
            fecha_inicio = request.POST.get("fecha_inicio")
            fecha_termino = request.POST.get("fecha_termino")
            hora_inicio = request.POST.get("hora_inicio")
            hora_termino = request.POST.get("hora_termino")

            # Combinar fecha y hora en objetos datetime "naive"
            fecha_inicio_completa = datetime.strptime(f"{fecha_inicio} {hora_inicio}", "%Y-%m-%d %H:%M")
            fecha_termino_completa = datetime.strptime(f"{fecha_termino} {hora_termino}", "%Y-%m-%d %H:%M")

            # Convertir a objetos datetime "aware"
            zonaH = pytz.timezone('America/Santiago')  # Reemplaza 'America/Santiago' con tu zona horaria
            fecha_inicio_aware = make_aware(fecha_inicio_completa, zonaH)
            fecha_termino_aware = make_aware(fecha_termino_completa, zonaH)

            campania_actual = campana.objects.last()

            if campania_actual:
                campania_actual.activo = False
                campania_actual.save()

            datos_campania = campana(
                nombre = nombre_campania,
                fecha_inicio = fecha_inicio_aware,
                fecha_final = fecha_termino_aware,
                activo = True
            )
            datos_campania.save()

            num_tabla_puntaje = puntaje.objects.all().count()

            if num_tabla_puntaje > 0:

                puntajes_actuales = puntaje.objects.all()

                for puntajes_actual in puntajes_actuales:
                    historial_puntaje.objects.create(
                        rut_ejecutivo = puntajes_actual.rut_ejecutivo,
                        fecha_inicio_camp = puntajes_actual.fecha_inicio_camp,
                        fecha_termino_camp = puntajes_actual.fecha_termino_camp,
                        puntaje_periodo = puntajes_actual.puntaje_periodo
                    )

                puntaje.objects.all().update(
                    puntaje_periodo = 0,
                    fecha_inicio_camp = fecha_inicio_aware,
                    fecha_termino_camp = fecha_termino_aware,
                    fecha_reset = timezone.now(),
                    fecha_movimiento = timezone.now()
                )
                messages.success(request, "Se reseteo la campaña exitosamente..")
            else:
                messages.error(request, "La tabla puntaje no posee registros..")


        except Exception as e:
            messages.error(request, f'Ocurrió un error: {str(e)}')
            return redirect('reset')
    return redirect('reset')