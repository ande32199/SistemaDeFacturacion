import wx
from clases_principales.crear_menu_secundario import PanelBase
from db_connection import Proveedor
from gestion_proveedor_categoria.formulario_proveedor import FormularioProveedor

class PanelProveedor(PanelBase):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Lista de proveedores
        self.list_control = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.list_control.InsertColumn(0, 'RUC', width=100)
        self.list_control.InsertColumn(1, 'Razón Social', width=200)
        self.list_control.InsertColumn(2, 'Teléfono', width=100)
        self.list_control.InsertColumn(3, 'Dirección', width=200)
        
        self.sizer.Add(self.list_control, 1, wx.EXPAND | wx.ALL, 5)
        
        # Vincular eventos
        self.btn_nuevo.Bind(wx.EVT_BUTTON, self.on_nuevo)
        self.btn_editar.Bind(wx.EVT_BUTTON, self.on_editar)
        self.btn_eliminar.Bind(wx.EVT_BUTTON, self.on_eliminar)
        
        self.actualizar_lista()
    
    def actualizar_lista(self):
        """Actualiza la lista de proveedores"""
        self.list_control.DeleteAllItems()
        proveedores = Proveedor.objects.all()
        for proveedor in proveedores:
            index = self.list_control.InsertItem(self.list_control.GetItemCount(), proveedor.ruc)
            self.list_control.SetItem(index, 1, proveedor.nombre)
            self.list_control.SetItem(index, 2, proveedor.telefono or "")
            self.list_control.SetItem(index, 3, proveedor.direccion or "")
    
    def on_nuevo(self, event):
        """Crear un nuevo proveedor"""
        try:
            formulario = FormularioProveedor(self, actualizar_lista_callback=self.actualizar_lista)
            formulario.agregar_botones(formulario.guardar_proveedor, lambda evt: formulario.Close())
            formulario.Show()
        except Exception as e:
            print(f"Error al abrir formulario: {str(e)}")
            wx.MessageBox(f"Error: {str(e)}", "Error", wx.ICON_ERROR)
    
    def on_editar(self, event):
        """Editar un proveedor existente"""
        selected = self.list_control.GetFirstSelected()
        if selected >= 0:
            ruc = self.list_control.GetItem(selected, 0).GetText()
            proveedor = Proveedor.objects.get(ruc=ruc)
            formulario = FormularioProveedor(
            self, 
            proveedor=proveedor, 
            title="Editar Proveedor",
            actualizar_lista_callback=self.actualizar_lista
            )
            formulario.agregar_botones(formulario.guardar_proveedor, lambda evt: formulario.Close())
            formulario.Show()
        else:
            wx.MessageBox("Seleccione un proveedor", "Error", wx.ICON_ERROR)
    
    def on_eliminar(self, event):
        """Eliminar un proveedor"""
        selected = self.list_control.GetFirstSelected()
        if selected >= 0:
            ruc = self.list_control.GetItem(selected, 0).GetText()
            if wx.MessageBox("¿Está seguro de eliminar este proveedor?", 
                             "Confirmar eliminación",
                             wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION) == wx.YES:
                proveedor = Proveedor.objects.get(ruc=ruc)
                proveedor.delete()
                self.actualizar_lista()
        else:
            wx.MessageBox("Seleccione un proveedor", "Error", wx.ICON_ERROR)
