import wx
from gestion.gestion_producto.producto import PanelProductos
from gestion.gestion_clientes.cliente import PanelClientes
from gestion.gestion_proveedor_categoria.ui_proveedor_categoria import PanelProveedor,PanelCategoria
from gestion.empresa.config import Configuraciones


class VentanaAdmin(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Sistema de Gestión - Administrador", size=(1024, 768))
        
        # Panel principal
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Crear el notebook (sistema de pestañas)
        self.notebook = wx.Notebook(self.panel)
        
        # Crear las páginas del notebook (con la pestaña de configuraciones primero)
        self.page_config = Configuraciones(self.notebook)
        self.page_clientes = PanelClientes(self.notebook)
        self.page_productos = PanelProductos(self.notebook)
        self.page_proveedores = PanelProveedor(self.notebook)
        self.page_categoria = PanelCategoria(self.notebook)
        
        # Añadir las páginas al notebook
        self.notebook.AddPage(self.page_config, "Configuraciones")
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
        super().__init__(parent, title="Inicio de Sesión - Administrador", size=(400, 275))
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Crear el sizer para el usuario
        sizer_usuario = wx.BoxSizer(wx.VERTICAL)
        self.lbl_usuario = wx.StaticText(self.panel, label="&Usuario:")
        self.txt_usuario = wx.TextCtrl(self.panel)
        sizer_usuario.Add(self.lbl_usuario, 0, wx.ALL, 5)
        sizer_usuario.Add(self.txt_usuario, 0, wx.EXPAND | wx.ALL, 5)
        
        # Crear el sizer para la contraseña oculta
        self.sizer_contrasena = wx.BoxSizer(wx.VERTICAL)
        self.lbl_contrasena = wx.StaticText(self.panel, label="&Contraseña:")
        self.txt_contrasena_oculta = wx.TextCtrl(self.panel, style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        self.sizer_contrasena.Add(self.lbl_contrasena, 0, wx.ALL, 5)
        self.sizer_contrasena.Add(self.txt_contrasena_oculta, 0, wx.EXPAND | wx.ALL, 5)

        # Crear el sizer para la contraseña visible
        self.txt_contrasena_visible = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.txt_contrasena_visible.Hide()
        self.sizer_contrasena.Add(self.txt_contrasena_visible, 0, wx.EXPAND | wx.ALL, 5)
        
        # Agregar los sizers al sizer principal
        self.sizer.Add(sizer_usuario, 0, wx.EXPAND | wx.ALL, 0)
        self.sizer.Add(self.sizer_contrasena, 0, wx.EXPAND | wx.ALL, 0)

        # Casilla de verificación para mostrar/ocultar contraseña
        self.chk_mostrar_contrasena = wx.CheckBox(self.panel, label="Mostrar Contraseña")
        self.sizer.Add(self.chk_mostrar_contrasena, 0, wx.ALL, 5)
        self.chk_mostrar_contrasena.Bind(wx.EVT_CHECKBOX, self.OnMostrarContrasena)

        # Botones
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_login = wx.Button(self.panel, label="Iniciar Sesión")
        self.btn_cancelar = wx.Button(self.panel, label="Cancelar")
        btn_sizer.Add(self.btn_login, 1, wx.EXPAND | wx.ALL, 5)
        btn_sizer.Add(self.btn_cancelar, 1, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(btn_sizer, 0, wx.CENTER)

        # Eventos
        self.txt_contrasena_oculta.Bind(wx.EVT_TEXT_ENTER, self.validar_login)
        self.txt_contrasena_visible.Bind(wx.EVT_TEXT_ENTER, self.validar_login)
        self.btn_login.Bind(wx.EVT_BUTTON, self.validar_login)
        self.btn_cancelar.Bind(wx.EVT_BUTTON, self.cancelar)

        self.panel.SetSizer(self.sizer)

        # Centrar la ventana en la pantalla
        self.Centre()

    def OnMostrarContrasena(self, event):
        """Mostrar u ocultar la contraseña según la casilla de verificación"""
        if self.chk_mostrar_contrasena.GetValue():
            self.txt_contrasena_visible.SetValue(self.txt_contrasena_oculta.GetValue())
            self.txt_contrasena_oculta.Hide()
            self.txt_contrasena_visible.Show()
            self.txt_contrasena_visible.SetFocus()
        else:
            self.txt_contrasena_oculta.SetValue(self.txt_contrasena_visible.GetValue())
            self.txt_contrasena_visible.Hide()
            self.txt_contrasena_oculta.Show()
            self.txt_contrasena_oculta.SetFocus()
        self.panel.Layout()

    def validar_login(self, event):
        """Validar usuario y contraseña"""
        username = self.txt_usuario.GetValue()
        if self.chk_mostrar_contrasena.GetValue():
            password = self.txt_contrasena_visible.GetValue()
        else:
            password = self.txt_contrasena_oculta.GetValue()
        
        if not username or not password:
            wx.MessageBox("Por favor ingrese usuario y contraseña", "Error", wx.ICON_ERROR)
            return
            
        from django.contrib.auth.hashers import check_password
        from gestion.db_connection import AdminPassword
        try:
            user = AdminPassword.objects.get(username=username)
            if check_password(password, user.password):
                self.EndModal(wx.ID_OK)
            else:
                wx.MessageBox("Contraseña incorrecta", "Error", wx.ICON_ERROR)
                if self.chk_mostrar_contrasena.GetValue():
                    self.txt_contrasena_visible.SetFocus()
                else:
                    self.txt_contrasena_oculta.SetFocus()
        except AdminPassword.DoesNotExist:
            wx.MessageBox("Usuario no encontrado", "Error", wx.ICON_ERROR)
            self.txt_usuario.SetFocus()

    def cancelar(self, event):
        self.EndModal(wx.ID_CANCEL)
