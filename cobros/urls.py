from django.urls import path
from .views import pagar_cobro, inicio

urlpatterns = [
    path('', inicio),

    path('pagar/<int:cobro_id>/', pagar_cobro, name='pagar_cobro'),
]