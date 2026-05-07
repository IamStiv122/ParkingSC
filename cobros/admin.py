from django.contrib import admin
from .models import Cliente, Vehiculo, EspacioEstacionamiento, Cobro

admin.site.register(Cliente)
admin.site.register(Vehiculo)
admin.site.register(EspacioEstacionamiento)
admin.site.register(TarifaHora)
admin.site.register(Cobro)