from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os
import wx
from gestion.db_connection import Producto, Proveedor, Categoria, Factura, DetalleFactura, Cliente, generar_factura
from decimal import Decimal

class MenuCompras(wx.Frame):
    def __init__(self, parent):
        super(MenuCompras, self).__init__(parent, title="Menu de Compras", size=(800, 600))
        self.carrito = []
        self.InitUI()
        self.Centre()
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def InitUI(self):
        panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Lista de productos
        self.list_control = wx.ListCtrl(panel, style=wx.LC_REPORT)
        self.list_control.InsertColumn(0, 'Código', width=80)
        self.list_control.InsertColumn(1, 'Nombre', width=150)
        self.list_control.InsertColumn(2, 'Precio', width=80)
        self.list_control.InsertColumn(3, 'Stock', width=80)
        self.list_control.InsertColumn(4, 'Categoría', width=120)
        self.list_control.InsertColumn(5, 'Proveedor', width=120)

        # Carrito de compras
        self.carrito_list = wx.ListCtrl(panel, style=wx.LC_REPORT)
        self.carrito_list.InsertColumn(0, 'Código', width=80)
        self.carrito_list.InsertColumn(1, 'Nombre', width=150)
        self.carrito_list.InsertColumn(2, 'Cantidad', width=80)
        self.carrito_list.InsertColumn(3, 'Precio Unit.', width=80)
        self.carrito_list.InsertColumn(4, 'Total', width=80)

        # Panel de cantidad
        cantidad_panel = wx.Panel(panel)
        cantidad_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cantidad_spin = wx.SpinCtrl(cantidad_panel, value='1', min=1, max=999)
        cantidad_sizer.Add(wx.StaticText(cantidad_panel, label="Cantidad:"), 0, wx.ALIGN_CENTER_VERTICAL)
        cantidad_sizer.Add(self.cantidad_spin, 0, wx.LEFT, 5)
        cantidad_panel.SetSizer(cantidad_sizer)

        # Botones
        button_panel = wx.Panel(panel)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.btn_agregar = wx.Button(button_panel, label="Agregar al Carrito")
        self.btn_quitar = wx.Button(button_panel, label="Quitar del Carrito")
        self.btn_facturar = wx.Button(button_panel, label="Facturar")
        self.btn_actualizar = wx.Button(button_panel, label="Actualizar Lista")
        
        button_sizer.Add(self.btn_agregar, 0, wx.RIGHT, 5)
        button_sizer.Add(self.btn_quitar, 0, wx.RIGHT, 5)
        button_sizer.Add(self.btn_facturar, 0, wx.RIGHT, 5)
        button_sizer.Add(self.btn_actualizar, 0)
        
        button_panel.SetSizer(button_sizer)

        # Eventos
        self.btn_agregar.Bind(wx.EVT_BUTTON, self.agregar_al_carrito)
        self.btn_quitar.Bind(wx.EVT_BUTTON, self.quitar_del_carrito)
        self.btn_facturar.Bind(wx.EVT_BUTTON, self.generar_factura)
        self.btn_actualizar.Bind(wx.EVT_BUTTON, self.actualizar_lista)

        # Layout
        self.sizer.Add(self.list_control, 1, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(cantidad_panel, 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(button_panel, 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.carrito_list, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(self.sizer)
        self.actualizar_lista(None)

    def on_close(self, event):
        self.Parent.Show()
        self.Destroy()
    def actualizar_lista(self, event):
        self.list_control.DeleteAllItems()
        productos = Producto.objects.all()
        
        for producto in productos:
            index = self.list_control.GetItemCount()
            self.list_control.InsertItem(index, producto.codigo)
            self.list_control.SetItem(index, 1, producto.nombre)
            self.list_control.SetItem(index, 2, str(producto.precio))
            self.list_control.SetItem(index, 3, str(producto.stock))
            self.list_control.SetItem(index, 4, producto.categoria.nombre if producto.categoria else '')
            self.list_control.SetItem(index, 5, producto.proveedor.nombre if producto.proveedor else '')

    def agregar_al_carrito(self, event):
        selected = self.list_control.GetFirstSelected()
        if selected == -1:
            wx.MessageBox('Seleccione un producto primero', 'Error', wx.OK | wx.ICON_ERROR)
            return

        codigo = self.list_control.GetItem(selected, 0).GetText()
        producto = Producto.objects.get(codigo=codigo)
        cantidad = self.cantidad_spin.GetValue()

        if cantidad > producto.stock:
            wx.MessageBox('No hay suficiente stock', 'Error', wx.OK | wx.ICON_ERROR)
            return

        # Agregar al carrito
        total = producto.precio * cantidad
        index = self.carrito_list.GetItemCount()
        self.carrito_list.InsertItem(index, codigo)
        self.carrito_list.SetItem(index, 1, producto.nombre)
        self.carrito_list.SetItem(index, 2, str(cantidad))
        self.carrito_list.SetItem(index, 3, str(producto.precio))
        self.carrito_list.SetItem(index, 4, str(total))

        self.carrito.append({
            'producto': producto,
            'cantidad': cantidad,
            'precio': producto.precio,
            'total': total
        })

    def quitar_del_carrito(self, event):
        selected = self.carrito_list.GetFirstSelected()
        if selected != -1:
            self.carrito_list.DeleteItem(selected)
            self.carrito.pop(selected)

    def generar_factura(self, event):
        if not self.carrito:
            wx.MessageBox('El carrito está vacío', 'Error', wx.OK | wx.ICON_ERROR)
            return

        # Diálogo para seleccionar cliente
        dlg = wx.TextEntryDialog(self, 'Ingrese la cédula del cliente:', 'Cliente')
        if dlg.ShowModal() == wx.ID_OK:
            try:
                cliente = Cliente.objects.get(cedula=dlg.GetValue())
                
                # Crear factura
                factura = Factura.objects.create(cliente=cliente)
                
                # Crear detalles
                for item in self.carrito:
                    DetalleFactura.objects.create(
                        factura=factura,
                        producto=item['producto'],
                        cantidad=item['cantidad']
                    )
                
                # Actualizar stock
                factura.actualizar_stock()
                
                # Limpiar carrito
                self.carrito = []
                self.carrito_list.DeleteAllItems()
                self.actualizar_lista(None)
                # generar el pdf con los detalles de la factura.
                self.generar_pdf_factura(factura)
                wx.MessageBox(f'Factura generada con éxito\nTotal: ${factura.total}', 'Éxito', wx.OK | wx.ICON_INFORMATION)
            
            except Cliente.DoesNotExist:
                wx.MessageBox('Cliente no encontrado', 'Error', wx.OK | wx.ICON_ERROR)
            except Exception as e:
                wx.MessageBox(f'Error al generar la factura: {str(e)}', 'Error', wx.OK | wx.ICON_ERROR)
        dlg.Destroy()

    def generar_pdf_factura(self, factura):
        from django.utils.timezone import localtime # importar la hora local de django para que la fecha sea correcta y acorde con la hora local.
        # Crear carpeta si no existe
        if not os.path.exists('facturas'):
            os.makedirs('facturas')

        # Ruta del PDF
        pdf_path = f"facturas/factura_{factura.id}.pdf"
        # Crear documento
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        elementos = []

        # Estilos
        styles = getSampleStyleSheet()
        estilo_titulo = styles['Heading1']
        estilo_texto = styles['Normal']

        # Encabezado
        titulo = Paragraph(f"Factura ID: {factura.id}", estilo_titulo)
        cliente = Paragraph(f"Cliente: {factura.cliente.nombre} {factura.cliente.apellido}", estilo_texto)
        fecha_formateada = localtime(factura.fecha).strftime('%d de %B de %Y %H:%M:%S') # Formatear la fecha a la hora local
        fecha = Paragraph(f"Fecha: {fecha_formateada}", estilo_texto)
        elementos.append(titulo)
        elementos.append(cliente)
        elementos.append(fecha)
        # Tabla de detalles
        data = [["Código", "Nombre", "Cantidad", "Precio Unitario", "Total"]]
        for detalle in factura.detalles.all():
            data.append([
                detalle.producto.codigo,
                detalle.producto.nombre,
                detalle.cantidad,
                f"${detalle.precio_unitario:.2f}",
                f"${detalle.precio_total:.2f}"
            ])

        # Totales
        data.append(["", "", "", "Subtotal", f"${factura.subtotal:.2f}"])
        data.append(["", "", "", "IVA", f"${factura.iva:.2f}"])
        data.append(["", "", "", "Total", f"${factura.total:.2f}"])
        # Crear tabla con estilos
        tabla = Table(data, colWidths=[80, 150, 80, 100, 100])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige, colors.lightgrey]),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 10)
        ]))
        elementos.append(tabla)
        # Crear PDF
        doc.build(elementos)
        wx.MessageBox(f"PDF de la factura generado exitosamente", 'Éxito', wx.OK | wx.ICON_INFORMATION)