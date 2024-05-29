#Desarrollado por Carolina Correa
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.contrib import messages
from App.inicial.models import premios,campana
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

@login_required
def premio(request):
    assert isinstance(request, HttpRequest)
    # Renderizar el template 'reporte/premio.html' y devolver la respuesta
    return render(request, 'premio/premio.html')

#Filtro de busqueda de campañas activas
@csrf_exempt
def buscar_campana(request):
    # Filtra las campañas que estén activas
    campanas_activas = campana.objects.filter(activo=True)

    # Crea una lista de diccionarios con los nombres de las campañas activas
    resultados = [{'nombre': c.nombre, 'activo': c.activo} for c in campanas_activas]

    # Devuelve los resultados en formato JSON
    return JsonResponse(resultados, safe=False)


#Agregar Premio a base de datos
@csrf_exempt
def agregar_premio(request):
    if request.method == 'POST':
        nombre_premio = request.POST.get('nombrePremio').upper()
        nombre_campana = request.POST.get('servicio')

        try:
            campana_obj = campana.objects.get(nombre=nombre_campana)
            premios.objects.create(
                premio=nombre_premio,
                fecha=timezone.now(),
                usuario=request.user,
                id_campana=campana_obj
            )
            messages.success(request, 'El premio se ha agregado correctamente.')
            return JsonResponse({'success': True, 'message': 'El premio se ha agregado correctamente.'})
        except campana.DoesNotExist:
            error_message = 'La campaña no existe.'
            messages.error(request, error_message)
            return JsonResponse({'success': False, 'message': error_message})
        except Exception as e:
            error_message = 'Error al agregar el premio.'
            messages.error(request, error_message)
            return JsonResponse({'success': False, 'message': error_message})

    return render(request, 'premio/premio.html')