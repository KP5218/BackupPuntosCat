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

    return render(request, 'premio/premio.html')

@csrf_exempt
def buscar_campana(request):
    nombre = request.GET.get('nombre', None)
    if nombre:
        campanas_filtradas = campana.objects.filter(nombre__icontains=nombre, activo=True)
        resultados = [{'nombre': c.nombre, 'activo': c.activo} for c in campanas_filtradas]
        print(resultados)
        return JsonResponse(resultados, safe=False)
    return JsonResponse([], safe=False)

@csrf_exempt
def agregar_premio(request):
    if request.method == 'POST':
        nombre_premio = request.POST.get('nombrePremio').upper()
        nombre_campana = request.POST.get('servicio')

        campana_obj = campana.objects.get(nombre=nombre_campana)

        try:
            nuevo_premio = premios.objects.create(
                premio=nombre_premio,
                fecha=timezone.now(),
                usuario=request.user if request.user.is_authenticated else None,
                id_campana=campana_obj
            )
            messages.success(request, 'El premio se ha agregado correctamente.')
        except Exception as e:
            messages.error(request, 'Error al agregar el premio')

        return redirect('premio')

    return render(request, 'premio/premio.html')
