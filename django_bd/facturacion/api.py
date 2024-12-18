from rest_framework.viewsets import ModelViewSet
from .models import Cliente,Proveedor,Producto,Factura,Categoria,DetalleFactura
from .serializers import ClienteSerializer,ProveedorSerializer,ProductoSerializer,CategoriaSerializer,FacturaSerializer,DetalleFacturaSerializer

class ClienteViewSet(ModelViewSet):
    queryset = Cliente.objects.all()  # Consulta para obtener todos los clientes
    serializer_class = ClienteSerializer

class ProductoViewSet(ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProveedorViewSet(ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer


class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class FacturaViewSet(ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer

class DetalleFacturaViewSet(ModelViewSet):
    queryset = DetalleFactura.objects.all()
    serializer_class = DetalleFacturaSerializer

