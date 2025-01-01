from django.contrib import admin
from .models import Cliente, Producto, Proveedor, Factura, DetalleFactura,AdminPassword, Categoria

admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(Factura)
admin.site.register(DetalleFactura)
admin.site.register(AdminPassword)
admin.site.register(Categoria)

