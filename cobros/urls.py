from django.urls import path
from .views import pagar_cobro

urlpatterns = [
    path('pagar/<int:cobro_id>/', pagar_cobro, name='pagar_cobro'),
]