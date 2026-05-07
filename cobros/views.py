from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse
from .models import Cobro
from django.http import HttpResponse

def inicio(request):
    return HttpResponse("Bienvenido a ParkingSC")

def pagar_cobro(request, cobro_id):
    cobro = get_object_or_404(Cobro, id=cobro_id)

    if not cobro.pagado:
        cobro.hora_salida = timezone.now()
        cobro.calcular_total()
        cobro.pagado = True
        cobro.espacio.estado = 'Libre'
        cobro.espacio.save()
        cobro.save()
        messages.success(request, f"Cobro {cobro.id} pagado. Total: ${cobro.total}")
    else:
        messages.info(request, f"El cobro {cobro.id} ya estaba pagado.")

    return redirect(reverse('admin:cobros_cobro_changelist'))
