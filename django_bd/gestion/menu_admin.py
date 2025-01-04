import wx
from gestion.gestion_producto.producto import PanelProductos
from gestion.gestion_clientes.cliente import PanelClientes
from gestion.gestion_proveedor_categoria.ui_proveedor_categoria import PanelProveedor,PanelCategoria



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
        self.page_categoria = PanelCategoria(self.notebook)
        
        # Añadir las páginas al notebook
        self.notebook.AddPage(self.page_clientes, "Gestión de Clientes")
        self.notebook.AddPage(self.page_productos, "Gestión de Productos")
        self.notebook.AddPage(self.page_proveedores, "Gestión de Proveedores")
        self.notebook.AddPage(self.page_categoria, "Gestión de Categorías")
        
        # Añadir el notebook al sizer principal
        self.sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)
        
        # Botón "Volver al Menú"
        btn_volver = wx.Button(self.panel, label="&Volver al Menú Principal")
        btn_volver.Bind(wx.EVT_BUTTON, self.volver_al_menu)
        self.sizer.Add(btn_volver, 0, wx.ALL | wx.CENTER, 10)
        
        # Configurar el panel principal
        self.panel.SetSizer(self.sizer)
        self.Centre()

    def volver_al_menu(self, event):
        """Volver a la ventana de bienvenida"""
        self.Hide()
        self.GetParent().Show()


class VentanaLogin(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Inicio de Sesión - Administrador", size=(400, 200))
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Etiqueta y campo de usuario
        lbl_usuario = wx.StaticText(panel, label="Usuario:")
        self.txt_usuario = wx.TextCtrl(panel)
        
        sizer.Add(lbl_usuario, 0, wx.ALL, 5)
        sizer.Add(self.txt_usuario, 0, wx.EXPAND | wx.ALL, 5)
        
        # Etiqueta y campo de contraseña
        lbl_contrasena = wx.StaticText(panel, label="Contraseña:")
        self.txt_contrasena = wx.TextCtrl(panel, style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        
        sizer.Add(lbl_contrasena, 0, wx.ALL, 5)
        sizer.Add(self.txt_contrasena, 0, wx.EXPAND | wx.ALL, 5)
        
        # Evento para presionar Enter en el campo de contraseña
        self.txt_contrasena.Bind(wx.EVT_TEXT_ENTER, self.validar_login)
        
        # Botones
        btn_login = wx.Button(panel, label="Iniciar Sesión")
        btn_cancelar = wx.Button(panel, label="Cancelar")
        btn_login.Bind(wx.EVT_BUTTON, self.validar_login)
        btn_cancelar.Bind(wx.EVT_BUTTON, self.cancelar)
        
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(btn_login, 1, wx.EXPAND | wx.ALL, 5)
        btn_sizer.Add(btn_cancelar, 1, wx.EXPAND | wx.ALL, 5)
        
        sizer.Add(btn_sizer, 0, wx.CENTER)
        panel.SetSizer(sizer)
        
    def validar_login(self, event):
        """Validar usuario y contraseña"""
        username = self.txt_usuario.GetValue()
        password = self.txt_contrasena.GetValue()
        from django.contrib.auth.hashers import check_password
        from gestion.db_connection import AdminPassword
        try:
            user = AdminPassword.objects.get(username=username)
            if check_password(password, user.password):
                self.EndModal(wx.ID_OK)
            else:
                wx.MessageBox("Contraseña incorrecta", "Error", wx.ICON_ERROR)
        except AdminPassword.DoesNotExist:
            wx.MessageBox("Usuario no encontrado", "Error", wx.ICON_ERROR)

    def cancelar(self, event):
        self.EndModal(wx.ID_CANCEL)
