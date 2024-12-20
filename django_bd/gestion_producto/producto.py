import wx
from clases_principales.crear_menu_secundario import PanelBase
from db_connection import Producto, Proveedor, Categoria
from gestion_producto.CrearActualizar import FormularioProducto

class PanelProductos(PanelBase):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Lista de productos
        self.list_control = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.list_control.InsertColumn(0, 'Código', width=80)
        self.list_control.InsertColumn(1, 'Nombre', width=150)
        self.list_control.InsertColumn(2, 'Precio', width=80)
        self.list_control.InsertColumn(3, 'Stock', width=80)
        self.list_control.InsertColumn(4, 'Categoría', width=120)
        self.list_control.InsertColumn(5, 'Proveedor', width=120)
        
        self.sizer.Add(self.list_control, 1, wx.EXPAND | wx.ALL, 5)
        
        # Vincular eventos
        self.btn_nuevo.Bind(wx.EVT_BUTTON, self.on_nuevo)
        self.btn_editar.Bind(wx.EVT_BUTTON, self.on_editar)
        self.btn_eliminar.Bind(wx.EVT_BUTTON, self.on_eliminar)
        
        self.actualizar_lista()
    
    def actualizar_lista(self):
        """Actualiza la lista de productos"""
        self.list_control.DeleteAllItems()
        productos = Producto.objects.all().select_related('categoria', 'proveedor')
        for producto in productos:
            categoria = producto.categoria.nombre if producto.categoria else "Sin categoría"
            proveedor = producto.proveedor.nombre if producto.proveedor else "Sin proveedor"
            index = self.list_control.InsertItem(self.list_control.GetItemCount(), producto.codigo)
            self.list_control.SetItem(index, 1, producto.nombre)
            self.list_control.SetItem(index, 2, f"${producto.precio}")
            self.list_control.SetItem(index, 3, str(producto.stock))
            self.list_control.SetItem(index, 4, categoria)
            self.list_control.SetItem(index, 5, proveedor)
    
    def on_nuevo(self, event):
        dlg = FormularioProducto(
            self, 
            title="Nuevo Producto",
            actualizar_lista_callback=self.actualizar_lista
        )
        dlg.ShowModal()
        dlg.Destroy()

    def on_eliminar(self, event):
        selected = self.list_control.GetFirstSelected()
        if selected >= 0:
            codigo = self.list_control.GetItem(selected, 0).GetText()
            if wx.MessageBox("¿Está seguro de eliminar este producto?", 
                           "Confirmar eliminación",
                           wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION) == wx.YES:
                producto = Producto.objects.get(codigo=codigo)
                producto.delete()
                self.actualizar_lista()
        else:
            wx.MessageBox("Seleccione un producto", "Error", wx.ICON_ERROR)

    def on_editar(self, event):
        selected = self.list_control.GetFirstSelected()
        if selected >= 0:
            try:
                codigo = self.list_control.GetItem(selected, 0).GetText()
                if not codigo:
                    wx.MessageBox("Error: Código de producto no válido", "Error", wx.ICON_ERROR)
                    return
                
                try:
                    producto = Producto.objects.get(codigo=codigo)
                    dlg = FormularioProducto(
                        self, 
                        title="Editar Producto", 
                        producto=producto,
                        actualizar_lista_callback=self.actualizar_lista
                    )
                    dlg.ShowModal()
                    dlg.Destroy()
                except Producto.DoesNotExist:
                    wx.MessageBox("No se encontró el producto en la base de datos", "Error", wx.ICON_ERROR)
            except Exception as e:
                wx.MessageBox(f"Error al abrir el producto: {str(e)}", "Error", wx.ICON_ERROR)
        else:
            wx.MessageBox("Seleccione un producto", "Error", wx.ICON_ERROR)