import wx
from gestion_producto.producto import PanelProductos
from gestion_clientes.cliente import PanelClientes
from gestion_proveedor_categoria.interface import PanelProveedor

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
        self.page_proveedores = PanelProveedor(self.notebook)
        
        # Añadir las páginas al notebook
        self.notebook.AddPage(self.page_inicio, "Inicio")
        self.notebook.AddPage(self.page_clientes, "Gestión de Clientes")
        self.notebook.AddPage(self.page_productos, "Gestión de Productos")
        self.notebook.AddPage(self.page_proveedores, "Gestión de Proveedores")
        
        # Configurar la página de inicio
        self.configurar_pagina_inicio()
        
        # Añadir el notebook al sizer principal
        self.sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)
        
        # Configurar el panel principal
        self.panel.SetSizer(self.sizer)
        
        self.Centre()
        
    def configurar_pagina_inicio(self):
        """Configura la página de inicio con información general y botón de salida"""
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Panel para el contenido con color de fondo
        panel_contenido = wx.Panel(self.page_inicio)
        panel_contenido.SetBackgroundColour(wx.Colour(240, 240, 240))  # Gris claro
        sizer_contenido = wx.BoxSizer(wx.VERTICAL)
        
        # Título
        titulo = wx.StaticText(panel_contenido, label="Sistema de Gestión")
        font_titulo = titulo.GetFont()
        font_titulo.SetPointSize(24)
        font_titulo.SetWeight(wx.FONTWEIGHT_BOLD)
        titulo.SetFont(font_titulo)
        titulo.SetForegroundColour(wx.Colour(50, 50, 50))  # Gris oscuro
        
        # Línea separadora
        linea = wx.StaticLine(panel_contenido)
        
        # Descripción del programa
        descripcion = """
Este sistema de gestión permite administrar eficientemente su negocio mediante:

• Gestión completa de clientes
    - Agregar nuevos clientes
    - Actualizar información existente
    - Consultar historial de clientes
    - Eliminar registros

• Control de inventario
    - Administrar productos
    - Gestionar stock
    - Controlar precios
    - Manejar categorías y proveedores

• Características adicionales
    - Interfaz intuitiva y fácil de usar
    - Sistema de pestañas integrado
    - Gestión centralizada
    - Respaldo de base de datos

Para comenzar, seleccione una de las pestañas superiores según la tarea que desee realizar.
        """
        
        texto_descripcion = wx.TextCtrl(panel_contenido, 
                                      value=descripcion,
                                      style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
        texto_descripcion.SetBackgroundColour(panel_contenido.GetBackgroundColour())
        font_descripcion = texto_descripcion.GetFont()
        font_descripcion.SetPointSize(11)
        texto_descripcion.SetFont(font_descripcion)
        
        # Información de versión y desarrollador
        info_version = wx.StaticText(panel_contenido, 
                                   label="Versión 1.0 | Desarrollado por [Roddy Romero]")
        font_version = info_version.GetFont()
        font_version.SetPointSize(9)
        info_version.SetFont(font_version)
        info_version.SetForegroundColour(wx.Colour(100, 100, 100))
        
        # Botón de salida
        btn_salir = wx.Button(panel_contenido, label="Salir del Programa", size=(150, 40))
        btn_salir.SetBackgroundColour(wx.Colour(220, 50, 50))  # Rojo
        btn_salir.SetForegroundColour(wx.WHITE)
        btn_salir.Bind(wx.EVT_BUTTON, self.salir_aplicacion)
        
        # Añadir widgets al sizer del contenido con espaciado
        sizer_contenido.Add(titulo, 0, wx.ALL | wx.CENTER | wx.EXPAND, 20)
        sizer_contenido.Add(linea, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        sizer_contenido.Add(texto_descripcion, 1, wx.ALL | wx.EXPAND, 20)
        sizer_contenido.Add(info_version, 0, wx.ALL | wx.CENTER, 10)
        sizer_contenido.Add(btn_salir, 0, wx.ALL | wx.CENTER, 20)
        
        # Configurar el panel de contenido
        panel_contenido.SetSizer(sizer_contenido)
        
        # Añadir el panel de contenido al sizer principal con margen
        sizer.Add(panel_contenido, 1, wx.EXPAND | wx.ALL, 20)
        
        # Configurar el sizer de la página
        self.page_inicio.SetSizer(sizer)
    
    def salir_aplicacion(self, event):
        """Método para cerrar la aplicación"""
        dlg = wx.MessageDialog(self, 
                             "¿Está seguro que desea salir del programa?",
                             "Confirmar Salida",
                             wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        
        if dlg.ShowModal() == wx.ID_YES:
            self.Close(True)
        
        dlg.Destroy()

