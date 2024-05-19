from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse,JsonResponse
import csv
from App.inicial.models import derivacion, puntaje
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime
@login_required
def index(request):
    assert isinstance(request, HttpRequest)

    return render(request, 'reporte/reporte.html')

@csrf_exempt
def buscar_resultados(request):
    if request.method == "POST":
        busqueda = request.POST.get("busqueda")
        fecha_inicio = request.POST.get("fechaInicio")
        fecha_fin = request.POST.get("fechaFin")

        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

        fecha_inicio = timezone.make_aware(fecha_inicio, timezone=timezone.utc)
        fecha_fin = timezone.make_aware(fecha_fin, timezone=timezone.utc)

        if busqueda == "derivacion":
            resultados = derivacion.objects.filter(fecha_derivacion__range=(fecha_inicio, fecha_fin))
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="resultados_derivacion.csv"'

            writer = csv.writer(response, delimiter=';')
            writer.writerow(['cod_derivacion', 'rut', 'nombre', 'direccion', 'telefono', 'correo', 'fecha_derivacion', 'derivador', 'derivado', 'observacion', 'fecha_derivacion_nueva', 'nuevo_derivador', 'cantidad_derivacion', 'correo_derivacion', 'correo_derivacion_nuevo', 'fecha_anulado', 'anulado'])

            for resultado in resultados:
                writer.writerow([
                    resultado.cod_derivacion,
                    resultado.rut,
                    resultado.nombre,
                    resultado.direccion,
                    resultado.telefono,
                    resultado.correo,
                    resultado.fecha_derivacion,
                    resultado.derivador,
                    resultado.derivado,
                    resultado.observacion,
                    resultado.fecha_derivacion_nueva,
                    resultado.nuevo_derivador,
                    resultado.cantidad_derivacion,
                    resultado.correo_derivacion,
                    resultado.correo_derivacion_nuevo,
                    resultado.fecha_anulado,
                    resultado.anulado
                ])

            return response
        elif busqueda == "puntaje":
            resultados = puntaje.objects.filter(fecha_inicio_camp__range=(fecha_inicio, fecha_fin))
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="resultados_puntaje.csv"'

            writer = csv.writer(response, delimiter=';')
            writer.writerow(['rut_ejecutivo', 'user_ejecutivo', 'n_personal', 'nombre_ejecutivo', 'puntaje_periodo', 'puntaje_acumulado_total', 'fecha_inicio_camp', 'fecha_termino_camp', 'fecha_reset', 'fecha_inicio_sistema', 'fecha_movimiento', 'fecha_anulado', 'anulado'])

            for resultado in resultados:
                writer.writerow([
                    resultado.rut_ejecutivo,
                    resultado.user_ejecutivo,
                    resultado.n_personal,
                    resultado.nombre_ejecutivo,
                    resultado.puntaje_periodo,
                    resultado.puntaje_acumulado_total,
                    resultado.fecha_inicio_camp,
                    resultado.fecha_termino_camp,
                    resultado.fecha_reset,
                    resultado.fecha_inicio_sistema,
                    resultado.fecha_movimiento,
                    resultado.fecha_anulado,
                    resultado.anulado
                ])

            return response

    return render(request, 'reporte.html')