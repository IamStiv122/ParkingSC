from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Cliente, Vehiculo, EspacioEstacionamiento, TarifaHora, Cobro

admin.site.register(Cliente)
admin.site.register(Vehiculo)
admin.site.register(EspacioEstacionamiento)
admin.site.register(TarifaHora)


@admin.register(Cobro)
class CobroAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'vehiculo', 'espacio', 'tarifa', 'hora_entrada',
        'hora_salida', 'horas', 'total', 'pagado', 'pagar_boton', 'eliminar_boton',
    )
    readonly_fields = ('horas', 'total', 'fecha', 'pagar_boton', 'eliminar_boton')
    search_fields = ('vehiculo__placa', 'vehiculo__cliente__nombre')

    def pagar_boton(self, obj):
        if obj and obj.pk and not obj.pagado:
            url = reverse('pagar_cobro', args=[obj.pk])
            return format_html('<a class="button" href="{}">PAGAR</a>', url)
        if obj and obj.pk and obj.pagado:
            return 'Pagado'
        return ''
    pagar_boton.short_description = 'Pagar'

    def eliminar_boton(self, obj):
        if obj and obj.pk:
            url = reverse('admin:cobros_cobro_delete', args=[obj.pk])
            return format_html('<a class="button" href="{}">ELIMINAR</a>', url)
        return ''
    eliminar_boton.short_description = 'Eliminar'
