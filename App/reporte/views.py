# Desarrollado por Carolina Correa
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
import csv
from App.inicial.models import derivacion, puntaje, campana
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime
from django.contrib import messages


@login_required
def index(request):
    assert isinstance(request, HttpRequest)
    # Renderizar el template 'reporte/reporte.html' y devolver la respuesta
    return render(request, 'reporte/reporte.html')
# Funcion busca datos en tabla derivacion, puntaje y crea el csv con estos datos
@csrf_exempt
def fecha_derivacion(fecha_inicio, fecha_fin):
    fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

    fecha_inicio = timezone.make_aware(fecha_inicio, timezone=timezone.utc)
    fecha_fin = timezone.make_aware(fecha_fin, timezone=timezone.utc)

    resultados = derivacion.objects.filter(fecha_derivacion__range=(fecha_inicio, fecha_fin)).order_by('-fecha_derivacion', '-rut')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_fecha_derivacion.csv"'
    response.write('\ufeff'.encode('utf8'))
    writer = csv.writer(response, delimiter=';')
    writer.writerow(
        ['NOMBRE CAMPAÑA', 'DERIVADOR', 'FECHA DERIVACION', 'CORREO DERIVACION',
         'DERIVADO', 'OBSERVACION', 'NUEVO DERIVADOR', 'FECHA DERIVACION NUEVA',
         'CORREO DERIVACION NUEVO', 'CANTIDAD DERIVACION', 'FECHA ANULADO', 'ANULADO'])

    for resultado in resultados:
        nombre_campana = resultado.campania.nombre if resultado.campania else ''
        fecha_derivacion = resultado.fecha_derivacion.strftime('%d-%m-%Y')
        fecha_derivacion_nueva = resultado.fecha_derivacion_nueva.strftime('%d-%m-%Y') if resultado.fecha_derivacion_nueva else ''
        fecha_anulado = resultado.fecha_anulado.strftime('%d-%m-%Y') if resultado.fecha_anulado else ''

        writer.writerow([
            nombre_campana,
            resultado.derivador,
            fecha_derivacion,
            resultado.correo_derivacion,
            resultado.derivado,
            resultado.observacion,
            resultado.nuevo_derivador,
            fecha_derivacion_nueva,
            resultado.correo_derivacion_nuevo,
            resultado.cantidad_derivacion,
            fecha_anulado,
            resultado.anulado
        ])

    return response

@csrf_exempt
def fecha_puntaje(fecha_inicio, fecha_fin):
    # Convertir las fechas de inicio y fin de cadenas de texto a objetos datetime
    fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

    # Hacer conscientes de la zona horaria las fechas convertidas
    fecha_inicio = timezone.make_aware(fecha_inicio, timezone=timezone.utc)
    fecha_fin = timezone.make_aware(fecha_fin, timezone=timezone.utc)

    # Filtrar los objetos de puntaje dentro del rango de fechas especificado
    resultados = puntaje.objects.filter(fecha_inicio_camp__range=(fecha_inicio, fecha_fin)).order_by('-fecha_inicio_camp','-puntaje_periodo')

    # Crear una respuesta HTTP con contenido tipo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_fecha_puntaje.csv"'
    response.write('\ufeff'.encode('utf8'))

    # Inicializar el escritor CSV
    writer = csv.writer(response, delimiter=';')

    # Escribir la fila de encabezado del CSV
    writer.writerow([
        'NOMBRE CAMPAÑA', 'RUT EJECUTIVO', 'NOMBRE EJECUTIVO',
        'PUNTAJE PERIODO', 'PUNTAJE ACUMULADO_TOTAL', 'FECHA INICIO_CAMPAÑA',
        'FECHA TERMINO CAMPAÑA', 'FECHA REINICIO', 'FECHA INICIO_SISTEMA',
        'FECHA MOVIMIENTO', 'FECHA ANULADO', 'ANULADO'
    ])

    # Iterar sobre los resultados y escribir cada fila en el CSV
    for resultado in resultados:
        nombre_campana = resultado.campania_id.nombre if resultado.campania_id else ''
        fecha_inicio_camp = resultado.fecha_inicio_camp.strftime('%d-%m-%Y')
        fecha_termino_camp = resultado.fecha_termino_camp.strftime('%d-%m-%Y') if resultado.fecha_termino_camp else ''
        fecha_reset = resultado.fecha_reset.strftime('%d-%m-%Y') if resultado.fecha_reset else ''
        fecha_inicio_sistema = resultado.fecha_inicio_sistema.strftime('%d-%m-%Y') if resultado.fecha_inicio_sistema else ''
        fecha_movimiento = resultado.fecha_movimiento.strftime('%d-%m-%Y') if resultado.fecha_movimiento else ''
        fecha_anulado = resultado.fecha_anulado.strftime('%d-%m-%Y') if resultado.fecha_anulado else ''

        writer.writerow([
            nombre_campana,
            resultado.rut_ejecutivo,
            resultado.nombre_ejecutivo,
            resultado.puntaje_periodo,
            resultado.puntaje_acumulado_total,
            fecha_inicio_camp,
            fecha_termino_camp,
            fecha_reset,
            fecha_inicio_sistema,
            fecha_movimiento,
            fecha_anulado,
            resultado.anulado,
        ])

    # Devolver la respuesta HTTP con el archivo CSV adjunto
    return response

@csrf_exempt
def fecha_campania(fecha_inicio, fecha_fin):
    fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

    fecha_inicio = timezone.make_aware(fecha_inicio, timezone=timezone.utc)
    fecha_fin = timezone.make_aware(fecha_fin, timezone=timezone.utc)

    resultados = campana.objects.filter(fecha_inicio__range=(fecha_inicio, fecha_fin)).order_by('-fecha_inicio')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="reporte_fecha_campania.csv"'
    response.write('\ufeff'.encode('utf8'))

    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'NOMBRE CAMPAÑA', 'FECHA DE INICIO', 'FECHA FINAL', 'ESTADO CAMPAÑA', 'RUT EJECUTIVO', 'NOMBRE EJECUTIVO',
        'EJECUTIVO', 'FECHA DERIVACION', 'EJECUTIVO NUEVO', 'FECHA NUEVA DERIVACION', 'CANTIDAD DERIVACION',
        'PUNTAJE ACUMULADO', 'PUNTAJE ACUMULADO TOTAL'
    ])

    for resultado in resultados:
        derivaciones = derivacion.objects.filter(campania_id=resultado.id)

        for deriv in derivaciones:
            fecha_derivacion_str = deriv.fecha_derivacion.strftime('%d-%m-%Y')
            fecha_nueva_derivacion_str = deriv.fecha_derivacion_nueva.strftime('%d-%m-%Y') if deriv.fecha_derivacion_nueva else ''

            puntajes = puntaje.objects.filter(user_ejecutivo=deriv.derivador)

            for punt in puntajes:
                writer.writerow([
                    resultado.nombre,
                    resultado.fecha_inicio.strftime('%d-%m-%Y'),
                    resultado.fecha_final.strftime('%d-%m-%Y'),
                    resultado.activo,
                    punt.rut_ejecutivo,
                    punt.nombre_ejecutivo,
                    deriv.derivador,
                    fecha_derivacion_str,
                    deriv.nuevo_derivador,
                    fecha_nueva_derivacion_str,
                    deriv.cantidad_derivacion,
                    punt.puntaje_periodo,
                    punt.puntaje_acumulado_total
                ])

    return response
@csrf_exempt
def campania_csv(nom_campania):
    resultados = campana.objects.filter(nombre=nom_campania).order_by('-fecha_inicio')
    if resultados:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="reporte_{nom_campania}.csv"'
        response.write('\ufeff'.encode('utf8'))

        writer = csv.writer(response, delimiter=';')
        writer.writerow([
            'NOMBRE CAMPAÑA', 'FECHA DE INICIO', 'FECHA FINAL', 'ESTADO CAMPAÑA','RUT EJECUTIVO', 'NOMBRE EJECUTIVO',
            'EJECUTIVO', 'FECHA DERIVACION', 'EJECUTIVO NUEVO', 'FECHA NUEVA DERIVACION', 'CANTIDAD DERIVACION',
            'PUNTAJE ACUMULADO', 'PUNTAJE ACUMULADO TOTAL'
        ])

        for resultado in resultados:
            derivaciones = resultado.derivacion_set.all()

            for derivacion in derivaciones:
                puntajes = puntaje.objects.filter(user_ejecutivo=derivacion.derivador)

                for puntaj in puntajes:
                    fecha_inicio = resultado.fecha_inicio.strftime('%d-%m-%Y')
                    fecha_final = resultado.fecha_final.strftime('%d-%m-%Y')
                    fecha_derivacion = derivacion.fecha_derivacion.strftime('%d-%m-%Y')
                    fecha_nueva_derivacion = derivacion.fecha_derivacion_nueva.strftime('%d-%m-%Y') if derivacion.fecha_derivacion_nueva else ''

                    writer.writerow([
                        resultado.nombre,
                        fecha_inicio,
                        fecha_final,
                        resultado.activo,
                        puntaj.rut_ejecutivo,
                        puntaj.nombre_ejecutivo,
                        derivacion.derivador,
                        fecha_derivacion,
                        derivacion.nuevo_derivador,
                        fecha_nueva_derivacion,
                        derivacion.cantidad_derivacion,
                        puntaj.puntaje_periodo,
                        puntaj.puntaje_acumulado_total
                    ])

        return response

@csrf_exempt
def buscar_detalles_campana(request):
    nombre = request.GET.get('nombre', None)
    if nombre:
        try:
            campana_obj = campana.objects.get(nombre=nombre)
            detalles = {
                'nombre': campana_obj.nombre,
                'fecha_inicio': campana_obj.fecha_inicio.strftime('%Y-%m-%d'),
                'fecha_fin': campana_obj.fecha_final.strftime('%Y-%m-%d')
            }
            return JsonResponse(detalles)
        except campana.DoesNotExist:
            return JsonResponse({'error': 'Campaña no encontrada'}, status=404)
    return JsonResponse({'error': 'Nombre no proporcionado'}, status=400)

@csrf_exempt
def buscar_campana(request):
    nombre = request.GET.get('nombre', None)
    if nombre:
        # Filtra las campañas por nombre que contenga el nombre proporcionado
        campanas_filtradas = campana.objects.filter(nombre__icontains=nombre).order_by('-fecha_inicio')
    else:
        # Obtiene todas las campañas sin filtrar por activo
        campanas_filtradas = campana.objects.all().order_by('-fecha_inicio')

    # Crea una lista de diccionarios con los resultados
    resultados = [{'nombre': c.nombre} for c in campanas_filtradas]
    return JsonResponse(resultados, safe=False)

@csrf_exempt
def csv_derivaciones(request):
    #Obtiene el valor del campo nombre-campania del formulario
    nombre_campania = request.POST.get('nombre-campania', '')

    #Buscar la campaña por su nombre
    try:
        campaña = campana.objects.get(nombre=nombre_campania)
    except campana.DoesNotExist:
        campaña = None

    #Filtrar derivaciones por el ID de la campaña si está presente
    if campaña:
        derivaciones = derivacion.objects.filter(campania_id=campaña.id).order_by('-fecha_derivacion', '-rut')
    else:
        derivaciones = derivacion.objects.all().order_by('-fecha_derivacion', '-rut')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_derivaciones.csv"'
    response.write('\ufeff'.encode('utf8'))

    writer = csv.writer(response, delimiter=';')
    writer.writerow(
        ['NOMBRE CAMPAÑA', 'DERIVADOR', 'FECHA DERIVACION', 'CORREO DERIVACION',
         'ESTADO DERIVACION', 'OBSERVACION', 'NUEVO DERIVADOR', 'FECHA DERIVACION NUEVA',
         'CORREO DERIVACION NUEVO', 'CANTIDAD DERIVACION', 'FECHA ANULADO', 'ANULADO'])

    for resultado in derivaciones:
        #Utiliza el valor del campo nombre-campania
        nombre_campana = nombre_campania if nombre_campania else (
            resultado.campania.nombre if resultado.campania else '')

        #Formatear las fechas para mostrar solo la parte de la fecha sin la hora
        fecha_derivacion = resultado.fecha_derivacion.strftime('%d-%m-%Y')
        fecha_derivacion_nueva = resultado.fecha_derivacion_nueva.strftime('%d-%m-%Y') if resultado.fecha_derivacion_nueva else ''
        fecha_anulado = resultado.fecha_anulado.strftime('%d-%m-%Y') if resultado.fecha_anulado else ''

        writer.writerow([
            nombre_campana,
            resultado.derivador,
            fecha_derivacion,
            resultado.correo_derivacion,
            resultado.derivado,
            resultado.observacion,
            resultado.nuevo_derivador,
            fecha_derivacion_nueva,
            resultado.correo_derivacion_nuevo,
            resultado.cantidad_derivacion,
            fecha_anulado,
            resultado.anulado
        ])

    return response
@csrf_exempt
def csv_puntaje(request):
    # Obtener el nombre de la campaña del formulario
    nombre_campania = request.POST.get('nombre-campania', '')

    # Buscar la campaña por su nombre
    try:
        campaña = campana.objects.get(nombre=nombre_campania)
    except campana.DoesNotExist:
        campaña = None

    # Filtrar puntajes por el ID de la campaña si está presente
    if campaña:
        puntajes = puntaje.objects.filter(campania_id=campaña.id).order_by('-puntaje_periodo', '-fecha_inicio_camp').order_by('-fecha_inicio_camp', '-puntaje_periodo')
    else:
        puntajes = puntaje.objects.all().order_by('-puntaje_periodo', '-fecha_inicio_camp').order_by('-fecha_inicio_camp', '-puntaje_periodo')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_puntajes.csv"'
    response.write('\ufeff'.encode('utf8'))

    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'NOMBRE CAMPAÑA', 'FECHA INICIO CAMPAÑA',
        'FECHA TERMINO CAMPAÑA', 'RUT EJECUTIVO', 'NOMBRE EJECUTIVO',
        'PUNTAJE PERIODO', 'PUNTAJE ACUMULADO TOTAL', 'FECHA REINICIO', 'FECHA INICIO SISTEMA',
        'FECHA MOVIMIENTO', 'FECHA ANULADO', 'ANULADO'
    ])

    for resultado in puntajes:
        nombre_campana = nombre_campania if nombre_campania else (
            resultado.campania_id.nombre if resultado.campania_id else '')

        # Formatear las fechas para mostrar solo la parte de la fecha sin la hora
        fecha_inicio_camp = resultado.fecha_inicio_camp.strftime('%d-%m-%Y')
        fecha_termino_camp = resultado.fecha_termino_camp.strftime('%d-%m-%Y') if resultado.fecha_termino_camp else ''
        fecha_reset = resultado.fecha_reset.strftime('%d-%m-%Y') if resultado.fecha_reset else ''
        fecha_inicio_sistema = resultado.fecha_inicio_sistema.strftime('%d-%m-%Y') if resultado.fecha_inicio_sistema else ''
        fecha_movimiento = resultado.fecha_movimiento.strftime('%d-%m-%Y') if resultado.fecha_movimiento else ''
        fecha_anulado = resultado.fecha_anulado.strftime('%d-%m-%Y') if resultado.fecha_anulado else ''

        writer.writerow([
            nombre_campana,
            fecha_inicio_camp,
            fecha_termino_camp,
            resultado.rut_ejecutivo,
            resultado.nombre_ejecutivo,
            resultado.puntaje_periodo,
            resultado.puntaje_acumulado_total,
            fecha_reset,
            fecha_inicio_sistema,
            fecha_movimiento,
            fecha_anulado,
            resultado.anulado,
        ])

    return response

@csrf_exempt
def csv_datos_cliente():
    derivaciones = derivacion.objects.all().order_by('-fecha_derivacion', '-rut')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_derivaciones_cliente.csv"'
    response.write('\ufeff'.encode('utf8'))

    writer = csv.writer(response, delimiter=';')
    writer.writerow(
        ['NOMBRE CLIENTE', 'RUT CLIENTE', 'TELEFONO CLIENTE', 'CORREO CLIENTE',
         'FECHA DERIVACION', 'CORREO DERIVACION NUEVO', 'FECHA DERIVACION NUEVA'
         ])

    for resultado in derivaciones:
        fecha_derivacion = resultado.fecha_derivacion.strftime('%d-%m-%Y')
        fecha_derivacion_nueva = resultado.fecha_derivacion_nueva.strftime('%d-%m-%Y') if resultado.fecha_derivacion_nueva else ''

        writer.writerow([
            resultado.nombre,
            resultado.rut,
            resultado.telefono,
            resultado.correo,
            fecha_derivacion,
            resultado.correo_derivacion_nuevo,
            fecha_derivacion_nueva
        ])

    return response

@csrf_exempt
def datos(request):
    if request.method == "POST":
        tipo_reporte = request.POST.get('eleccion')
        tipo_busqueda = request.POST.get('busqueda')
        fecha_inicio = request.POST.get('fechaInicio')
        fecha_fin = request.POST.get('fechaFin')
        nombre_campania = request.POST.get('nombre-campania')
        tipo_select = request.POST.get('tipo-detalle')

        if tipo_reporte == 'campana' and tipo_busqueda == 'campana' and tipo_select == 'campana':
            return campania_csv(nombre_campania)

        elif tipo_reporte == 'campana' and tipo_busqueda == 'campana' and tipo_select == 'derivacion':
            return csv_derivaciones(request)

        elif tipo_reporte == 'campana' and tipo_busqueda == 'campana' and tipo_select == 'puntaje':
            return csv_puntaje(request)

        elif tipo_reporte == 'campana' and tipo_busqueda == 'Cliente':
            return csv_datos_cliente()

        elif tipo_reporte == 'fecha' and tipo_busqueda == 'derivacion':
            return fecha_derivacion(fecha_inicio, fecha_fin)

        elif tipo_reporte == 'fecha' and tipo_busqueda == 'puntaje':
            return fecha_puntaje(fecha_inicio, fecha_fin)

        elif tipo_reporte == 'fecha' and tipo_busqueda == 'campana':
            return fecha_campania(fecha_inicio, fecha_fin)

    return redirect('index')
