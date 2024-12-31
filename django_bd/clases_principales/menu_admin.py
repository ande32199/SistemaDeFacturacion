import wx
from gestion_producto.producto import PanelProductos
from gestion_clientes.cliente import PanelClientes
from gestion_proveedor_categoria.interface import PanelProveedor



class VentanaAdmin(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Sistema de Gestión - Administrador", size=(1024, 768))
        
        # Panel principal
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Crear el notebook (sistema de pestañas)
        self.notebook = wx.Notebook(self.panel)
        
        # Crear las páginas del notebook (sin "Inicio")
        self.page_clientes = PanelClientes(self.notebook)
        self.page_productos = PanelProductos(self.notebook)
        self.page_proveedores = PanelProveedor(self.notebook)
        
        # Añadir las páginas al notebook
        self.notebook.AddPage(self.page_clientes, "Gestión de Clientes")
        self.notebook.AddPage(self.page_productos, "Gestión de Productos")
        self.notebook.AddPage(self.page_proveedores, "Gestión de Proveedores")
        
        # Añadir el notebook al sizer principal
        self.sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)
        
        # Botón "Volver al Menú"
        btn_volver = wx.Button(self.panel, label="Volver al Menú Principal")
        btn_volver.Bind(wx.EVT_BUTTON, self.volver_al_menu)
        self.sizer.Add(btn_volver, 0, wx.ALL | wx.CENTER, 10)
        
        # Configurar el panel principal
        self.panel.SetSizer(self.sizer)
        self.Centre()

    def volver_al_menu(self, event):
        """Volver a la ventana de bienvenida"""
        self.Hide()
        self.GetParent().Show()
