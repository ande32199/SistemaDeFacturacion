import wx
from gestion.crear_menu_secundario import PanelBase
from gestion.db_connection import ObtenerClientes, Cliente
from gestion.gestion_clientes.agregar_cliente import AgregarCliente
from gestion.gestion_clientes.actualiza import ActualizaCliente

class PanelClientes(PanelBase):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Lista de clientes
        self.list_control = wx.ListBox(self)
        self.sizer.Add(self.list_control, 1, wx.EXPAND | wx.ALL, 5)
        
        # Vincular eventos
        self.btn_nuevo.Bind(wx.EVT_BUTTON, self.on_nuevo)
        self.btn_editar.Bind(wx.EVT_BUTTON, self.on_editar)
        self.btn_eliminar.Bind(wx.EVT_BUTTON, self.on_eliminar)
        
        self.actualizar_lista()
    
    def actualizar_lista(self):
        """Actualiza la lista de clientes"""
        self.list_control.Clear()
        clientes = ObtenerClientes()
        for cliente in clientes:
            self.list_control.Append(cliente)
    
    def on_nuevo(self, event):
        AgregarCliente(actualizar_lista_callback=self.actualizar_lista)
    
    def on_editar(self, event):
        selection = self.list_control.GetSelection()
        if selection != wx.NOT_FOUND:
            cliente_str = self.list_control.GetString(selection)
            cedula = cliente_str.split(" ")[0]
            try:
                cliente = Cliente.objects.get(cedula=cedula)
                ActualizaCliente(cliente,actualizar_lista_callback=self.actualizar_lista)
                self.actualizar_lista()
            except Cliente.DoesNotExist:
                wx.MessageBox("Cliente no encontrado", "Error", wx.ICON_ERROR)
        else:
            wx.MessageBox("Seleccione un cliente", "Error", wx.ICON_ERROR)
    
    def on_eliminar(self, event):
        selection = self.list_control.GetSelection()
        if selection != wx.NOT_FOUND:
            cliente_str = self.list_control.GetString(selection)
            cedula = cliente_str.split(" ")[0]
            try:
                cliente = Cliente.objects.get(cedula=cedula)
                if wx.MessageBox("¿Está seguro de eliminar este cliente?", 
                               "Confirmar eliminación",
                               wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION) == wx.YES:
                    cliente.delete()
                    self.actualizar_lista()
            except Cliente.DoesNotExist:
                wx.MessageBox("Cliente no encontrado", "Error", wx.ICON_ERROR)
        else:
            wx.MessageBox("Seleccione un cliente", "Error", wx.ICON_ERROR)
