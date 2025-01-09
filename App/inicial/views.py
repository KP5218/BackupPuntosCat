import smtplib
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import choice
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from App.inicial.models import premios, campana, derivacion_rechazada, historial_puntaje
from django.contrib import messages
from django.utils import timezone
from App.cliente.models import Basecliente
from App.inicial.models import derivacion, puntaje, correo

# Create your views here.

def home(request):
    # Verifica que el objeto 'request' sea una instancia de 'HttpRequest'
    assert isinstance(request, HttpRequest)

    # Obtiene el nombre de usuario del usuario logueado y la fecha actual
    usuario_logeado = request.user.username
    fecha_hoy = date.today()

    # Obtiene la última campaña activa (si existe alguna)
    ultima_campana = campana.objects.filter(activo=True).first()
    hoy = date.today()

    # Inicializa variables para evitar errores si no hay una campaña activa
    fecha_inicio_sin_hora = ""
    fecha_final_sin_hora = ""
    resultados_combinados_sorted = ""
    posicion_usuario=""
    registros_top_5=""
    posicion_usuario_hoy=""

    # Si hay una campaña activa
    if ultima_campana:
        # Verifica si la fecha de hoy está dentro del rango de fechas de la campaña activa
        if ultima_campana.fecha_inicio.date() <= hoy <= ultima_campana.fecha_final.date():

            # Obtiene el ranking de hoy
            resultados_combinados_sorted = obtener_ranking_hoy(fecha_hoy)

            # Obtiene la posición del usuario en el ranking
            posicion_usuario = posicion_usuario_ranking(usuario_logeado)

            # Obtiene el top 5 del ranking del periodo
            registros_top_5 = top5_ranking_periodo()

            # Obtiene la posición diaria del usuario
            posicion_usuario_hoy = posicion_usuario_diario(fecha_hoy, usuario_logeado)

            # Formatea las fechas de inicio y final de la campaña (si existen) en 'dd-mm-YYYY'
            fecha_inicio_sin_hora = ultima_campana.fecha_inicio.strftime(
                '%d-%m-%Y') if ultima_campana.fecha_inicio else None

            fecha_final_sin_hora = ultima_campana.fecha_final.strftime(
                '%d-%m-%Y') if ultima_campana.fecha_final else None

            # Imprime un mensaje de depuración indicando que hoy está dentro del rango de la campaña activa
            print("¡Hoy está dentro del rango de la última campaña activa!")
        else:
            # Imprime un mensaje de depuración indicando que hoy no está dentro del rango de la campaña activa
            print("Hoy NO está dentro del rango de la última campaña activa.")
            respuesta= desactivar_campania(ultima_campana,hoy)

            if respuesta:
                if respuesta.fecha_inicio.date() <= hoy <= respuesta.fecha_final.date():
                    # Obtiene el ranking de hoy
                    resultados_combinados_sorted = obtener_ranking_hoy(fecha_hoy)

                    # Obtiene la posición del usuario en el ranking
                    posicion_usuario = posicion_usuario_ranking(usuario_logeado)

                    # Obtiene el top 5 del ranking del periodo
                    registros_top_5 = top5_ranking_periodo()

                    # Obtiene la posición diaria del usuario
                    posicion_usuario_hoy = posicion_usuario_diario(fecha_hoy, usuario_logeado)

                    # Formatea las fechas de inicio y final de la campaña (si existen) en 'dd-mm-YYYY'
                    fecha_inicio_sin_hora = respuesta.fecha_inicio.strftime(
                        '%d-%m-%Y') if respuesta.fecha_inicio else None

                    fecha_final_sin_hora = respuesta.fecha_final.strftime(
                        '%d-%m-%Y') if respuesta.fecha_final else None

    else:
        camp_actual = puntaje.objects.filter(anulado=False, campania_id__isnull=False).first()

        if camp_actual:
            resultado= prox_campana(hoy,camp_actual)

            if resultado:
                if resultado.fecha_inicio.date() <= hoy <= resultado.fecha_final.date():
                    # Obtiene el ranking de hoy
                    resultados_combinados_sorted = obtener_ranking_hoy(fecha_hoy)

                    # Obtiene la posición del usuario en el ranking
                    posicion_usuario = posicion_usuario_ranking(usuario_logeado)

                    # Obtiene el top 5 del ranking del periodo
                    registros_top_5 = top5_ranking_periodo()

                    # Obtiene la posición diaria del usuario
                    posicion_usuario_hoy = posicion_usuario_diario(fecha_hoy, usuario_logeado)

                    # Formatea las fechas de inicio y final de la campaña (si existen) en 'dd-mm-YYYY'
                    fecha_inicio_sin_hora = resultado.fecha_inicio.strftime(
                        '%d-%m-%Y') if resultado.fecha_inicio else None

                    fecha_final_sin_hora = resultado.fecha_final.strftime(
                        '%d-%m-%Y') if resultado.fecha_final else None
        else:
            proxima_campana = campana.objects.filter(fecha_inicio__gte=hoy).order_by('fecha_inicio').first()
            resultado = prox_campana(hoy, proxima_campana)

            if resultado:
                if resultado.fecha_inicio.date() <= hoy <= resultado.fecha_final.date():
                    # Obtiene el ranking de hoy
                    resultados_combinados_sorted = obtener_ranking_hoy(fecha_hoy)

                    # Obtiene la posición del usuario en el ranking
                    posicion_usuario = posicion_usuario_ranking(usuario_logeado)

                    # Obtiene el top 5 del ranking del periodo
                    registros_top_5 = top5_ranking_periodo()

                    # Obtiene la posición diaria del usuario
                    posicion_usuario_hoy = posicion_usuario_diario(fecha_hoy, usuario_logeado)

                    # Formatea las fechas de inicio y final de la campaña (si existen) en 'dd-mm-YYYY'
                    fecha_inicio_sin_hora = resultado.fecha_inicio.strftime(
                        '%d-%m-%Y') if resultado.fecha_inicio else None

                    fecha_final_sin_hora = resultado.fecha_final.strftime(
                        '%d-%m-%Y') if resultado.fecha_final else None


    # Renderiza la plantilla 'app/index.html' pasando las variables al contexto
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

#Funcion para verificar si hay una campaña activa el dia actual
def prox_campana(hoy,camp_actual):
    proxima_campana = campana.objects.filter(fecha_inicio__gte=hoy).order_by('fecha_inicio').first()

    if proxima_campana:
        if proxima_campana.fecha_inicio.date() == hoy:
            # Guarda las fechas de la próxima campaña
            fecha_inicio = proxima_campana.fecha_inicio
            fecha_final = proxima_campana.fecha_final

            
            # Llama a la función reset_camp con las nuevas fechas
            try:
                # Intentar acceder a 'campania_id'
                campania_id = camp_actual.campania_id
            except AttributeError:
                # Si el atributo no existe, establecer campania_id como None
                campania_id = None

            # Verificar si campania_id tiene un valor válido
            if campania_id:
                reset_camp(fecha_inicio, fecha_final, proxima_campana, campania_id)
            else:

                reset_camp(fecha_inicio, fecha_final, proxima_campana, camp_actual)

            proxima_campana.activo = True
            proxima_campana.save()

        return proxima_campana
    return False

#Funcion que desactiva la campaña actual si es necesario
#y verifico si para el dia actual se debe activar una funcion
def desactivar_campania(ultima_campana, hoy):
    ultima_campana.activo = False
    ultima_campana.save()

    proxima_campana = campana.objects.filter(fecha_inicio__gte=hoy).order_by('fecha_inicio').first()
    if proxima_campana:
        if proxima_campana.fecha_inicio.date() == hoy:
            proxima_campana.activo = True
            proxima_campana.save()

            # Guarda las fechas de la próxima campaña
            fecha_inicio = proxima_campana.fecha_inicio
            fecha_final = proxima_campana.fecha_final

            # Llama a la función reset_camp con las nuevas fechas
            reset_camp(fecha_inicio, fecha_final, proxima_campana, ultima_campana)
            return proxima_campana
        else:
            return False
    else:
        return False

#Funcion para resetear la campaña y guardar en el historial
def reset_camp(fecha_inicio, fecha_final,proxima_campana,ultima_campana):
    # contamos los registros en la tabla de puntajes
    num_tabla_puntaje = puntaje.objects.all().count()

    if num_tabla_puntaje > 0:
        # Obtenemos todos los puntajes actuales
        puntajes_actuales = puntaje.objects.all()

        # Guardamos los puntajes actuales en el historial de puntajes
        for puntajes_actual in puntajes_actuales:
            historial_puntaje.objects.create(
                rut_ejecutivo=puntajes_actual.rut_ejecutivo,
                fecha_inicio_camp=puntajes_actual.fecha_inicio_camp,
                fecha_termino_camp=puntajes_actual.fecha_termino_camp,
                puntaje_periodo=puntajes_actual.puntaje_periodo,
                campania_id=ultima_campana.id
            )

        # Reseteamos los valores de la tabla puntajes y actualizamos las fechas
        puntaje.objects.all().update(
            puntaje_periodo=0,
            fecha_inicio_camp=fecha_inicio,
            fecha_termino_camp=fecha_final,
            fecha_reset=timezone.now(),
            fecha_movimiento=timezone.now(),
            campania_id=proxima_campana.id
        )

        return True

def top5_ranking_periodo():
    #sentencia para obtener los top 5
    registros_top_5 = puntaje.objects.exclude(puntaje_periodo=None).order_by('-puntaje_periodo')[:5]

    return registros_top_5

def posicion_usuario_ranking(usuario_logeado):
    #La posicion del usuario en el ranking global
    registros_top = puntaje.objects.exclude(puntaje_periodo=None).exclude(puntaje_periodo=0).order_by('-puntaje_periodo')

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
        fecha_derivacion_nueva__date=fecha_hoy
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
    #posicion del usuario en el ranking diario
    derivaciones_hoy = derivacion.objects.filter(
        Q(fecha_derivacion__date=fecha_hoy) | Q(fecha_derivacion_nueva__date=fecha_hoy)
    )

    # Anotamos los conteos separados por derivador y nuevo_derivador
    derivaciones_contadas = derivaciones_hoy.annotate(
        cuenta_derivador=Count('id', filter=Q(fecha_derivacion__date=fecha_hoy)),
        cuenta_nuevo_derivador=Count('id', filter=Q(fecha_derivacion_nueva__date=fecha_hoy))
    )

    # Diccionario para almacenar los resultados
    resultados = {}
    for derivaciones in derivaciones_contadas:
        if derivaciones.derivador:
            if derivaciones.derivador not in resultados:
                resultados[derivaciones.derivador] = 0
            resultados[derivaciones.derivador] += derivaciones.cuenta_derivador

        if derivaciones.nuevo_derivador:
            if derivaciones.nuevo_derivador not in resultados:
                resultados[derivaciones.nuevo_derivador] = 0
            resultados[derivaciones.nuevo_derivador] += derivaciones.cuenta_nuevo_derivador

    # Convertimos los resultados en una lista ordenada por total_registros
    ejecutivos_top_hoy = sorted(resultados.items(), key=lambda item: item[1], reverse=True)

    # Encontramos la posición del usuario logeado
    posicion_usuario_hoy = None
    for index, (ejecutivo, total) in enumerate(ejecutivos_top_hoy, start=1):
        if ejecutivo == usuario_logeado:
            posicion_usuario_hoy = index
            break

    return posicion_usuario_hoy

def exit(request):
    logout(request)
    return redirect('home')


def insertar_derivacion(request):
    if request.method == 'POST':
        try:
            checkbox = request.POST.get("rechaza_seguro")
            if checkbox:
                rechazo_seguro = deriv_rechazada(request)
                messages.success(request, 'El cliente ha rechazado el seguro alemana.')
                return redirect('home')
            else:
                rut = request.POST.get('rut')
                nombre = request.POST.get('nombre')
                telefono = request.POST.get('telefono')
                email = request.POST.get('email')
                usuario = request.user

                puntaje_existente = puntaje.objects.filter(user_ejecutivo=usuario.username, anulado=False).first()

                if not puntaje_existente:
                    messages.error(request, 'El usuario no está habilitado para derivar.')
                    return redirect('home')

                derivacion_existente = derivacion.objects.filter(rut=rut).first()

                correo_destino, nombre_destino = obtener_correo_aleatorio()

                if derivacion_existente:
                    if derivacion_existente.cantidad_derivacion < 2:
                        observacion = request.POST.get('observacion')

                        derivacion_existente.nombre = nombre
                        derivacion_existente.correo = email
                        derivacion_existente.telefono = telefono
                        derivacion_existente.fecha_derivacion_nueva = timezone.now()
                        derivacion_existente.nuevo_derivador = usuario.username
                        derivacion_existente.cantidad_derivacion = 2
                        derivacion_existente.correo_derivacion_nuevo = correo_destino
                        derivacion_existente.observacion = observacion

                        # Obtiene la campaña activa
                        campana_activa = campana.objects.filter(activo=True).latest('fecha_inicio')
                        derivacion_existente.campania = campana_activa

                        derivacion_existente.save()

                        envio_correo_individual(correo_destino, nombre_destino, nombre, rut, email, telefono)
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
                        telefono=telefono,
                        correo=email,
                        derivador=usuario,
                        cantidad_derivacion=1,
                        correo_derivacion=correo_destino
                    )

                    # Obtiene la campaña activa
                    campana_activa = campana.objects.filter(activo=True).latest('fecha_inicio')
                    datos_derivacion.campania = campana_activa

                    datos_derivacion.save()

                    envio_correo_individual(correo_destino, nombre_destino, nombre, rut, email, telefono)

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
    #funcion para obtener correo aleatorio
    correos_validos = correo.objects.filter(valido=True)

    if correos_validos.exists():
        correo_aleatorio = choice(correos_validos)

        print(f"Correo aleatorio: {correo_aleatorio.correo}")

        return  correo_aleatorio.correo, correo_aleatorio.nombre
    else:
        print("No hay correos válidos en la base de datos.")

def envio_correo_individual(correo_destino,nombre_destino,nombre_cliente,rut_cliente,email,telefono):
    # Configuración del servidor SMTP
    smtp_server = "smtp.itdchile.cl"
    smtp_port = 46500
    smtp_username = 'jruizt'
    smtp_password = 'Kic1905$'

    # Creación de un objeto mensaje
    mensaje = MIMEMultipart()
    mensaje["From"] = 'clinica@alemanatemuco.cl'
    mensaje["To"] = correo_destino
    mensaje["Subject"] = f"Correo derivacion CAT- {telefono}- {nombre_cliente} "

    # Creación del cuerpo del mensaje en formato HTML
    saludo = f"Estimado/a {nombre_destino},<br>"  # Puedes ajustar el saludo según el género del destinatario

    contenido_mensaje = (
        f"{saludo}"
        "&nbsp;&nbsp;&nbsp;&nbsp; A continuación, le proporciono los datos del cliente para seguro alemana:<br><br>"
        f"&nbsp;&nbsp;&nbsp;&nbsp;<b>Rut:</b> {rut_cliente}<br>"
        f"&nbsp;&nbsp;&nbsp;&nbsp;<b>Nombre:</b> {nombre_cliente}<br>"
        f"&nbsp;&nbsp;&nbsp;&nbsp;<b>telefono:</b> {telefono}<br>"
        f"&nbsp;&nbsp;&nbsp;&nbsp;<b>correo:</b> {email}<br><br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Atentamente,<br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Clinica Alemana Temuco"
    )

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
    #funcion para mostrar premios en template
    campanas_activas = campana.objects.filter(activo=True, premios__isnull=False).distinct()

    lista_premios = []

    for campana_activa in campanas_activas:
        premios_campaña = premios.objects.filter(id_campana=campana_activa)
        for premio in premios_campaña:
            lista_premios.append(premio.premio)

    return JsonResponse({'premios': lista_premios})


def busqueda_cliente(request,rut_cliente):
    #funcion para buscarel cliente
    datos_cliente = derivacion.objects.filter(rut=rut_cliente, anulado=False)
    datacli = list(datos_cliente.values())
    return JsonResponse(datacli, safe=False)

def cliente_rechazo(request,rut_cliente):
    #funcion para buscarel cliente en tabla de rechazos de derivacion
    datos_cliente = derivacion_rechazada.objects.filter(rut=rut_cliente, anulado=False)
    datacli = list(datos_cliente.values())
    return JsonResponse(datacli, safe=False)

def deriv_rechazada(request):
    rut = request.POST.get('rut')
    usuario = request.user

    datos_rechazo = derivacion_rechazada(
        rut=rut,
        ejecutivo=usuario,
    )
    datos_rechazo.save()

    return True