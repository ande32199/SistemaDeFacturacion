import wx
from gestion_producto.producto import PanelProductos
from gestion_clientes.cliente import PanelClientes

class VentanaPrincipal(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Sistema de Gestión", size=(1024, 768))
        
        # Panel principal
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Crear el notebook (sistema de pestañas)
        self.notebook = wx.Notebook(self.panel)
        
        # Crear las páginas del notebook
        self.page_inicio = wx.Panel(self.notebook)
        self.page_clientes = PanelClientes(self.notebook)
        self.page_productos = PanelProductos(self.notebook)
        
        # Añadir las páginas al notebook
        self.notebook.AddPage(self.page_inicio, "Inicio")
        self.notebook.AddPage(self.page_clientes, "Gestión de Clientes")
        self.notebook.AddPage(self.page_productos, "Gestión de Productos")
        
        # Configurar la página de inicio
        self.configurar_pagina_inicio()
        
        # Añadir el notebook al sizer principal
        self.sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)
        
        # Configurar el panel principal
        self.panel.SetSizer(self.sizer)
        
        self.Centre()
        
    def configurar_pagina_inicio(self):
        """Configura la página de inicio con información general"""
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Título
        titulo = wx.StaticText(self.page_inicio, label="Sistema de Gestión")
        font = titulo.GetFont()
        font.SetPointSize(14)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        titulo.SetFont(font)
        
        # Añadir widgets a la página de inicio
        sizer.Add(titulo, 0, wx.ALL | wx.CENTER, 20)
        
        # Configurar el sizer de la página
        self.page_inicio.SetSizer(sizer)