from django.contrib import admin
from .models import Cliente, Producto, Proveedor, Factura, DetalleFactura

admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(Factura)
admin.site.register(DetalleFactura)
