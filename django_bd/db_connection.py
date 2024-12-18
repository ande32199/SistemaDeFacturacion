import os
import django
from django.conf import settings

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_bd.settings')
django.setup()

from facturacion.models import Cliente,Proveedor,Categoria,Producto

def ObtenerClientes():
    return [f"{cliente.cedula} - {cliente.nombre} {cliente.apellido}" for cliente in Cliente.objects.all()]

def ObtenerCategorias():
    return [f"{Categoria.nombre} - {Categoria.descripcion}" for categoria in Categoria.objects.all()]