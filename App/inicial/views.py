import smtplib
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import choice

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.db.models import Count
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from App.inicial.models import derivacion, puntaje
from App.inicial.models import premios, campana
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from django.utils import timezone

from App.cliente.models import Basecliente
from App.inicial.models import derivacion, puntaje, correo


# Create your views here.

def home(request):
    assert isinstance(request, HttpRequest)

    usuario_logeado = request.user.username
    fecha_hoy = date.today()

    ultima_campana = campana.objects.filter(activo=True).first()
    hoy = date.today()

    fecha_inicio_sin_hora = ""
    fecha_final_sin_hora = ""
    resultados_combinados_sorted = ""
    posicion_usuario=""
    registros_top_5=""
    posicion_usuario_hoy=""

    if ultima_campana:
        if ultima_campana.fecha_inicio <= hoy <= ultima_campana.fecha_final:

            resultados_combinados_sorted = obtener_ranking_hoy(fecha_hoy)
            posicion_usuario = posicion_usuario_ranking(usuario_logeado)

            registros_top_5 = top5_ranking_periodo()

            posicion_usuario_hoy = posicion_usuario_diario(fecha_hoy, usuario_logeado)

            fecha_inicio_sin_hora = ultima_campana.fecha_inicio.strftime(
                '%d-%m-%Y') if ultima_campana.fecha_inicio else None
            fecha_final_sin_hora = ultima_campana.fecha_final.strftime(
                '%d-%m-%Y') if ultima_campana.fecha_final else None

            print("¡Hoy está dentro del rango de la última campaña activa!")
        else:
            print("Hoy NO está dentro del rango de la última campaña activa.")

    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'puntaje_periodo':registros_top_5,
            'ejecutivos_top_hoy':resultados_combinados_sorted,
            'posicion_usuario_hoy':posicion_usuario_hoy,
            'posicion_usuario':posicion_usuario,
            'fecha_fin': fecha_final_sin_hora
        }
    )

def top5_ranking_periodo():
    registros_top_5 = puntaje.objects.exclude(puntaje_periodo=None).order_by('-puntaje_periodo')[:5]

    return registros_top_5

def posicion_usuario_ranking(usuario_logeado):
    registros_top = puntaje.objects.exclude(puntaje_periodo=None).order_by('-puntaje_periodo')

    posicion_usuario = None
    for index, registro in enumerate(registros_top):
        if registro.user_ejecutivo == usuario_logeado:
            posicion_usuario = index + 1
            break
    return posicion_usuario

def obtener_ranking_hoy(fecha_hoy):
    # Consulta para obtener el total de registros por derivador para hoy
    ejecutivos_total_hoy = derivacion.objects.filter(
        fecha_derivacion__date=fecha_hoy
    ).exclude(
        derivador__isnull=True
    ).values(
        'derivador'
    ).annotate(
        total_registros=Count('id')
    )

    # Consulta para obtener el total de registros por nuevo_derivador para hoy
    nuevos_derivadores_total_hoy = derivacion.objects.filter(
        fecha_derivacion__date=fecha_hoy
    ).exclude(
        nuevo_derivador__isnull=True
    ).values(
        'nuevo_derivador'
    ).annotate(
        total_registros=Count('id')
    )

    # Crear un diccionario para almacenar y sumar los total_registros por ejecutivo
    ejecutivos_dict = {}

    # Agregar total_registros de derivadores a ejecutivos_dict
    for item in ejecutivos_total_hoy:
        ejecutivo = item['derivador']
        total_registros = item['total_registros']
        if ejecutivo in ejecutivos_dict:
            ejecutivos_dict[ejecutivo] += total_registros
        else:
            ejecutivos_dict[ejecutivo] = total_registros

    # Agregar total_registros de nuevos_derivadores a ejecutivos_dict
    for item in nuevos_derivadores_total_hoy:
        ejecutivo = item['nuevo_derivador']
        total_registros = item['total_registros']
        if ejecutivo in ejecutivos_dict:
            ejecutivos_dict[ejecutivo] += total_registros
        else:
            ejecutivos_dict[ejecutivo] = total_registros

    # Convertir ejecutivos_dict en una lista de diccionarios para ordenar
    resultados_combinados = [
        {'ejecutivo': key, 'total_registros': value}
        for key, value in ejecutivos_dict.items()
    ]

    # Ordenar la lista combinada por total_registros en orden descendente
    resultados_combinados_sorted = sorted(
        resultados_combinados,
        key=lambda x: x['total_registros'],
        reverse=True
    )[:5]

    return resultados_combinados_sorted

def posicion_usuario_diario(fecha_hoy,usuario_logeado):
    ejecutivos_top_hoy = derivacion.objects.filter(fecha_derivacion__date=fecha_hoy).values('derivador').annotate(
        total_registros=Count('id')).order_by('-total_registros')

    posicion_usuario_hoy = None
    for index, ejecutivo in enumerate(ejecutivos_top_hoy):
        if ejecutivo['derivador'] == usuario_logeado:
            posicion_usuario_hoy = index + 1
            break
    return posicion_usuario_hoy

def exit(request):
    logout(request)
    return redirect('home')


def insertar_derivacion(request):
    if request.method == 'POST':
        try:
            rut = request.POST.get('rut')
            nombre = request.POST.get('nombre')
            direccion = request.POST.get('direccion')
            telefono = request.POST.get('telefono')
            email = request.POST.get('email')
            usuario = request.user

            puntaje_existente = puntaje.objects.filter(user_ejecutivo=usuario.username,anulado=False).first()

            if not puntaje_existente:
                messages.error(request, 'El usuario no está habilitado para derivar.')
                return redirect('home')

            derivacion_existente = derivacion.objects.filter(rut=rut).first()

            correo_destino, nombre_destino = obtener_correo_aleatorio()

            if derivacion_existente:
                if derivacion_existente.cantidad_derivacion < 2:
                    observacion = request.POST.get('observacion')

                    derivacion_existente.nombre = nombre
                    derivacion_existente.direccion = direccion
                    derivacion_existente.correo = email
                    derivacion_existente.telefono = telefono
                    derivacion_existente.fecha_derivacion_nueva = timezone.now()
                    derivacion_existente.nuevo_derivador = usuario.username
                    derivacion_existente.cantidad_derivacion = 2
                    derivacion_existente.correo_derivacion_nuevo = correo_destino
                    derivacion_existente.observacion = observacion
                    derivacion_existente.save()

                    envio_correo_individual(correo_destino,nombre_destino,nombre,rut,email,direccion,telefono)

                else:
                    messages.error(request, 'Este cliente ya ha sido derivado anteriormente.')
                    return redirect('home')
            else:
                ultima_derivacion = derivacion.objects.order_by('-cod_derivacion').first()
                if ultima_derivacion:
                    siguiente_cod = ultima_derivacion.cod_derivacion + 1
                else:
                    siguiente_cod = 1  

                datos_derivacion = derivacion(
                    cod_derivacion=siguiente_cod,
                    rut=rut,
                    nombre=nombre,
                    direccion=direccion,
                    telefono=telefono,
                    correo=email,
                    derivador=usuario,
                    cantidad_derivacion=1,
                    correo_derivacion=correo_destino

                )
                datos_derivacion.save()
                envio_correo_individual(correo_destino,nombre_destino,nombre,rut,email,direccion,telefono)

            if puntaje_existente:
                if puntaje_existente.puntaje_periodo is None:
                    puntaje_existente.puntaje_periodo = 0
                if puntaje_existente.puntaje_acumulado_total is None:
                    puntaje_existente.puntaje_acumulado_total = 0

                puntaje_existente.puntaje_periodo += 1
                puntaje_existente.puntaje_acumulado_total += 1
                puntaje_existente.fecha_movimiento = timezone.now()
                puntaje_existente.save()

            messages.success(request, 'La derivación se realizó con éxito.')
            return redirect('home')

        except Exception as e:
            messages.error(request, f'Ocurrió un error: {str(e)}')
            return redirect('home')

    messages.error(request, 'Método no permitido.')
    return redirect('home')


def obtener_correo_aleatorio():
    correos_validos = correo.objects.filter(valido=True)

    if correos_validos.exists():
        correo_aleatorio = choice(correos_validos)

        print(f"Correo aleatorio: {correo_aleatorio.correo}")

        return  correo_aleatorio.correo, correo_aleatorio.nombre
    else:
        print("No hay correos válidos en la base de datos.")

def envio_correo_individual(correo_destino,nombre_destino,nombre_cliente,rut_cliente,email,direccion,telefono):
    # Configuración del servidor SMTP
    smtp_server = "smtp.itdchile.cl"
    smtp_port = 46500
    smtp_username = 'jruizt'
    smtp_password = 'Kic1905$'

    # Creación de un objeto mensaje
    mensaje = MIMEMultipart()
    mensaje["From"] = 'clinica@alemanatemuco.cl'
    mensaje["To"] = correo_destino
    mensaje["Subject"] = 'Correo derivacion'

    # Creación del cuerpo del mensaje en formato HTML
    saludo = f"Estimado/a {nombre_destino},<br>"  # Puedes ajustar el saludo según el género del destinatario

    contenido_mensaje = (
        f"{saludo}"
        "&nbsp;&nbsp;&nbsp;&nbsp; A continuación, le proporciono los datos del cliente para seguro alemana:<br><br>"
        f"&nbsp;&nbsp;&nbsp;&nbsp;<b>Rut:</b> {rut_cliente}<br>"
        f"&nbsp;&nbsp;&nbsp;&nbsp;<b>Nombre:</b> {nombre_cliente}<br>"
        f"&nbsp;&nbsp;&nbsp;&nbsp;<b>Direccion:</b> {direccion}<br>"
        f"&nbsp;&nbsp;&nbsp;&nbsp;<b>telefono:</b> {telefono}<br>"
        f"&nbsp;&nbsp;&nbsp;&nbsp;<b>correo:</b> {email}<br><br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Atentamente,<br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Clinica Alemana Temuco"
    )

    # Creación de un objeto mensaje
    mensaje = MIMEMultipart()
    mensaje["From"] = 'clinica@alemanatemuco.cl'
    mensaje["To"] = correo_destino
    mensaje["Subject"] = 'Correo derivacion'

    # Adjuntando texto al correo electrónico como HTML
    mensaje.attach(MIMEText(contenido_mensaje, "html"))

    try:
        # Intento de conexión al servidor SMTP y envío del correo electrónico
        with smtplib.SMTP(smtp_server, smtp_port) as servidor_smtp:
            servidor_smtp.login(smtp_username, smtp_password)
            servidor_smtp.sendmail(mensaje["From"], mensaje["To"], mensaje.as_string())

            # Si el correo se envía correctamente, muestra un mensaje de éxito
            print("Correo enviado correctamente.")

    except Exception as e:
        # Si ocurre un error durante el envío del correo, muestra un mensaje de error
        print(f"Error al enviar el correo electrónico: {e}")

    # Devuelve True para indicar el estado del envío del correo electrónico
    return True

def filtrocliente(request, rut_cliente):
    datos_cliente = Basecliente.objects.filter(rut=rut_cliente)
    datacli = list(datos_cliente.values())
    return JsonResponse(datacli, safe=False)



@login_required()
def mostrar_premio(request):
    campanas_activas = campana.objects.filter(activo=True, premios__isnull=False).distinct()

    lista_premios = []

    for campana_activa in campanas_activas:
        premios_campaña = premios.objects.filter(id_campana=campana_activa)
        for premio in premios_campaña:
            lista_premios.append(premio.premio)

    return JsonResponse({'premios': lista_premios})


def busqueda_cliente(request,rut_cliente):
    datos_cliente = derivacion.objects.filter(rut=rut_cliente, anulado=False)
    datacli = list(datos_cliente.values())
    return JsonResponse(datacli, safe=False)

