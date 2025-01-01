import os
import django
import wx
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_bd.settings')
django.setup()

from facturacion.models import Cliente, Producto, Factura, DetalleFactura

class SistemaVentas(wx.Frame):
    def __init__(self, parent, title):
        super(SistemaVentas, self).__init__(parent, title=title, size=(800, 600))
        self.carrito = {}  # Diccionario para almacenar los productos seleccionados
        self.InitUI()
        self.Center()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)

        # Layout principal
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Lista de productos
        self.productos_list = wx.ListBox(panel)
        vbox.Add(self.productos_list, proportion=2, flag=wx.EXPAND | wx.ALL, border=10)

        # Botones para agregar productos al carrito
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.codigo_txt = wx.TextCtrl(panel, size=(150, -1), placeholder="Código del producto")
        self.cantidad_txt = wx.TextCtrl(panel, size=(150, -1), placeholder="Cantidad")
        agregar_btn = wx.Button(panel, label="Agregar al carrito")
        agregar_btn.Bind(wx.EVT_BUTTON, self.agregar_al_carrito)

        hbox1.Add(self.codigo_txt, flag=wx.RIGHT, border=10)
        hbox1.Add(self.cantidad_txt, flag=wx.RIGHT, border=10)
        hbox1.Add(agregar_btn, flag=wx.RIGHT, border=10)

        vbox.Add(hbox1, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=10)

        # Lista del carrito
        self.carrito_list = wx.ListBox(panel)
        vbox.Add(self.carrito_list, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # Botones de acciones finales
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        finalizar_btn = wx.Button(panel, label="Finalizar Compra")
        finalizar_btn.Bind(wx.EVT_BUTTON, self.finalizar_compra)
        salir_btn = wx.Button(panel, label="Salir")
        salir_btn.Bind(wx.EVT_BUTTON, self.salir)

        hbox2.Add(finalizar_btn, flag=wx.RIGHT, border=10)
        hbox2.Add(salir_btn, flag=wx.RIGHT, border=10)

        vbox.Add(hbox2, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        panel.SetSizer(vbox)

        # Cargar productos al iniciar
        self.cargar_productos()

    def cargar_productos(self):
        """Carga los productos disponibles desde la base de datos en la lista."""
        self.productos_list.Clear()
        productos = Producto.objects.filter(stock__gt=0)  # Solo productos con stock disponible
        for producto in productos:
            self.productos_list.Append(f"Código: {producto.codigo} | {producto.nombre} | Precio: ${producto.precio:.2f} | Stock: {producto.stock}")

    def agregar_al_carrito(self, event):
        """Agrega un producto al carrito de compras."""
        codigo = self.codigo_txt.GetValue().strip()
        cantidad = self.cantidad_txt.GetValue().strip()

        if not codigo or not cantidad:
            wx.MessageBox("Debe ingresar el código y la cantidad.", "Error", wx.ICON_ERROR)
            return

        try:
            cantidad = int(cantidad)
            producto = Producto.objects.get(codigo=codigo)

            if cantidad > producto.stock:
                wx.MessageBox(f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}.", "Error", wx.ICON_ERROR)
                return

            # Agregar al carrito
            if codigo in self.carrito:
                self.carrito[codigo]['cantidad'] += cantidad
            else:
                self.carrito[codigo] = {'producto': producto, 'cantidad': cantidad}

            self.carrito_list.Append(f"{producto.nombre} x {cantidad}")
            wx.MessageBox(f"{cantidad} unidad(es) de {producto.nombre} agregado(s) al carrito.", "Éxito", wx.ICON_INFORMATION)
        except Producto.DoesNotExist:
            wx.MessageBox("El producto no existe.", "Error", wx.ICON_ERROR)
        except ValueError:
            wx.MessageBox("La cantidad debe ser un número entero.", "Error", wx.ICON_ERROR)

    def finalizar_compra(self, event):
        """Finaliza la compra y genera la factura."""
        if not self.carrito:
            wx.MessageBox("El carrito está vacío. Agregue productos antes de finalizar la compra.", "Error", wx.ICON_ERROR)
            return

        cedula = wx.GetTextFromUser("Ingrese la cédula del cliente:", "Finalizar Compra")

        try:
            cliente = Cliente.objects.get(cedula=cedula)
        except Cliente.DoesNotExist:
            wx.MessageBox("El cliente no existe. Regístrelo antes de continuar.", "Error", wx.ICON_ERROR)
            return

        # Crear factura
        factura = Factura(cliente=cliente)
        factura.save()

        # Procesar carrito
        total = 0
        for item in self.carrito.values():
            producto = item['producto']
            cantidad = item['cantidad']
            precio_total = producto.precio * cantidad

            DetalleFactura.objects.create(
                factura=factura,
                producto=producto,
                cantidad=cantidad,
                precio_total=precio_total,
            )

            # Actualizar stock
            producto.stock -= cantidad
            producto.save()

            total += precio_total

        # Actualizar totales de la factura
        factura.subtotal = total
        factura.iva = total * Decimal('0.15')  # 15% IVA
        factura.total = factura.subtotal + factura.iva
        factura.save()

        # Mostrar factura
        detalles = "\n".join([f"{item['producto'].nombre} x {item['cantidad']} - ${item['producto'].precio * item['cantidad']:.2f}" for item in self.carrito.values()])
        wx.MessageBox(f"Factura generada exitosamente.\n\nDetalles:\n{detalles}\n\nSubtotal: ${factura.subtotal:.2f}\nIVA: ${factura.iva:.2f}\nTotal: ${factura.total:.2f}", "Factura", wx.ICON_INFORMATION)

        # Limpiar carrito
        self.carrito.clear()
        self.carrito_list.Clear()
        self.cargar_productos()

    def salir(self, event):
        """Cierra la aplicación."""
        self.Close()

if __name__ == "__main__":
    app = wx.App()
    SistemaVentas(None, title="Sistema de Ventas")
    app.MainLoop()
