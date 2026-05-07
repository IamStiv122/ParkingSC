from django.db import models
from decimal import Decimal
from django.utils import timezone


# CLIENTE
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10, unique=True)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre


# VEHÍCULO
class Vehiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    placa = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=50)
    color = models.CharField(max_length=30)

    def __str__(self):
        return self.placa


# ESPACIO DE ESTACIONAMIENTO
class EspacioEstacionamiento(models.Model):
    ESTADOS = [
        ('Libre', 'Libre'),
        ('Ocupado', 'Ocupado'),
    ]

    numero = models.IntegerField(unique=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Libre')

    def __str__(self):
        return f"Espacio {self.numero}"


# TARIFA POR HORA
class TarifaHora(models.Model):
    nombre = models.CharField(max_length=50)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - ${self.valor}"


# COBRO / FACTURA
class Cobro(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    espacio = models.ForeignKey(EspacioEstacionamiento, on_delete=models.CASCADE)
    tarifa = models.ForeignKey(TarifaHora, on_delete=models.PROTECT)

    hora_entrada = models.DateTimeField(default=timezone.now)
    hora_salida = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Si el auto acaba de ingresar, no rellene hora de salida."
    )

    horas = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    pagado = models.BooleanField(default=False)

    fecha = models.DateField(auto_now_add=True)

    def calcular_total(self):
        if self.hora_salida:
            diferencia = self.hora_salida - self.hora_entrada
            horas = Decimal(diferencia.total_seconds()) / Decimal(3600)
            self.horas = round(horas, 2)
            self.total = round(horas * self.tarifa.valor, 2)

    def save(self, *args, **kwargs):
        if self.hora_salida:
            self.calcular_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cobro #{self.id} - {self.vehiculo.placa}"
