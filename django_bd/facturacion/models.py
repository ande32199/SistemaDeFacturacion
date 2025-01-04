from django.db import models
from django.contrib.auth.hashers import make_password
from decimal import Decimal

class AdminPassword(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Almacena contraseñas hasheadas

    def save(self, *args, **kwargs):
        # Asegurarse de que la contraseña esté encriptada antes de guardarla
        if not self.password.startswith('pbkdf2_'):  # Evitar volver a encriptar si ya está hasheada
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    cedula = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Proveedor(models.Model):
    ruc = models.CharField(max_length=13, primary_key=True)
    nombre = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.ruc} {self.nombre}"

class Producto(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Factura(models.Model):
    PORCENTAJE_IVA = Decimal('0.15')  # 15% del IVA puede ser modificable
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calcular_totales(self):
        # Calcular subtotal
        self.subtotal = sum(detalle.precio_total for detalle in self.detalles.all())
        # Calcular IVA
        self.iva = self.subtotal * self.PORCENTAJE_IVA
        # Calcular total
        self.total = self.subtotal + self.iva
        self.save()

    def actualizar_stock(self):
        for detalle in self.detalles.all():
            detalle.producto.stock -= detalle.cantidad
            detalle.producto.save()

    def __str__(self):
        return f"Factura {self.id} - {self.cliente.nombre} {self.cliente.apellido}"

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Calcular precio total del detalle
        self.precio_unitario = self.producto.precio
        self.precio_total = self.precio_unitario * self.cantidad
        super().save(*args, **kwargs)
        # Actualizar totales de la factura
        self.factura.calcular_totales()

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"