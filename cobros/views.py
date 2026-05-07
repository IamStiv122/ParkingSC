from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from .models import Cobro
from django.http import HttpResponse

def inicio(request):
    return HttpResponse("Bienvenido a ParkingSC")

def pagar_cobro(request, cobro_id):

    cobro = get_object_or_404(Cobro, id=cobro_id)

    cobro.hora_salida = timezone.now()

    cobro.calcular_total()

    cobro.pagado = True

    cobro.espacio.estado = 'Libre'
    cobro.espacio.save()

    cobro.save()

    return redirect('/admin')