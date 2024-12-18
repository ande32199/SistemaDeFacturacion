from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import ClienteViewSet, ProductoViewSet, ProveedorViewSet, CategoriaViewSet, FacturaViewSet,DetalleFacturaViewSet

# Configura un router para las rutas de la API
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'proveedores', ProveedorViewSet, basename='proveedor')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'facturas', FacturaViewSet, basename='factura')
router.register(r'detalles-facturas', DetalleFacturaViewSet, basename='detalle-factura')


urlpatterns = [
    path('', include(router.urls)),  # Incluye todas las rutas generadas por el router
]
