import wx
import os
from gestion.menu_admin import VentanaAdmin, VentanaLogin
from gestion.menu_compras import MenuCompras

class VentanaBienvenida(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Bienvenido al Sistema", size=(500, 400))
        
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(240, 240, 240))  # Fondo suave
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Fuente para título
        font = wx.Font(20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        # Sombra del título
        sombra_titulo = wx.StaticText(panel, label="Bienvenido al Sistema de Ventas")
        sombra_titulo.SetFont(font)
        sombra_titulo.SetForegroundColour(wx.Colour(100, 100, 100))  # Gris oscuro
        sombra_titulo.SetPosition((11, 21))  # Posición desplazada para la sombra
        
        # Título principal
        titulo = wx.StaticText(panel, label="Bienvenido al Sistema de Ventas")
        titulo.SetFont(font)
        titulo.SetForegroundColour(wx.Colour(33, 47, 61))  # Texto oscuro
        titulo.SetBackgroundColour(wx.Colour(255, 223, 186))  # Fondo naranja claro
        titulo.SetWindowStyle(wx.BORDER_SIMPLE)  # Borde alrededor
        titulo.SetPosition((10, 20))  # Posición principal
        
        # Imagen
        try:
            ruta_imagen = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.jpg")
            image = wx.Image(ruta_imagen, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            image_ctrl = wx.StaticBitmap(panel, wx.ID_ANY, image)
        except Exception as e:
            wx.MessageBox(f"No se pudo cargar la imagen: {e}", "Error", wx.ICON_ERROR)
            image_ctrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(1, 1))  # Imagen vacía
        
        # Botones de opciones
        btn_admin = wx.Button(panel, label="Entrar como &Administrador", size=(200, 50))
        btn_compras = wx.Button(panel, label="Entrar al menú de &compras", size=(200, 50))
        btn_salir = wx.Button(panel, label="&Salir", size=(200, 50))
        
        # Colores iniciales de los botones
        self.configurar_boton(btn_admin, wx.Colour(41, 128, 185), wx.Colour(255, 255, 255))  # Azul
        self.configurar_boton(btn_compras, wx.Colour(39, 174, 96), wx.Colour(255, 255, 255))  # Verde
        self.configurar_boton(btn_salir, wx.Colour(192, 57, 43), wx.Colour(255, 255, 255))  # Rojo
        
        # Eventos de hover
        btn_admin.Bind(wx.EVT_ENTER_WINDOW, lambda evt: self.on_hover_enter(evt, btn_admin, wx.Colour(93, 173, 226)))  # Azul claro
        btn_admin.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.on_hover_leave(evt, btn_admin, wx.Colour(41, 128, 185)))  # Azul original
        btn_compras.Bind(wx.EVT_ENTER_WINDOW, lambda evt: self.on_hover_enter(evt, btn_compras, wx.Colour(82, 190, 128)))  # Verde claro
        btn_compras.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.on_hover_leave(evt, btn_compras, wx.Colour(39, 174, 96)))  # Verde original
        btn_salir.Bind(wx.EVT_ENTER_WINDOW, lambda evt: self.on_hover_enter(evt, btn_salir, wx.Colour(231, 76, 60)))  # Rojo claro
        btn_salir.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.on_hover_leave(evt, btn_salir, wx.Colour(192, 57, 43)))  # Rojo original
        
        # Enlazar eventos de clic
        btn_admin.Bind(wx.EVT_BUTTON, self.entrar_como_admin)
        btn_compras.Bind(wx.EVT_BUTTON, self.entrar_como_cliente)
        btn_salir.Bind(wx.EVT_BUTTON, self.salir)
        
        # Añadir widgets al sizer
        sizer.Add(titulo, 0, wx.ALL | wx.CENTER, 20)
        sizer.Add(image_ctrl, 0, wx.ALL | wx.CENTER, 20)
        sizer.Add(btn_admin, 0, wx.ALL | wx.CENTER, 10)
        sizer.Add(btn_compras, 0, wx.ALL | wx.CENTER, 10)
        sizer.Add(btn_salir, 0, wx.ALL | wx.CENTER, 10)
        
        panel.SetSizer(sizer)
        self.Centre()
    
    # Configuración inicial de botones
    def configurar_boton(self, boton, color_fondo, color_texto):
        boton.SetBackgroundColour(color_fondo)
        boton.SetForegroundColour(color_texto)
    
    # Evento al pasar el cursor sobre el botón
    def on_hover_enter(self, event, button, color_hover):
        button.SetBackgroundColour(color_hover)
        button.Refresh()
    
    # Evento al salir el cursor del botón
    def on_hover_leave(self, event, button, color_original):
        button.SetBackgroundColour(color_original)
        button.Refresh()

    def entrar_como_admin(self, event):
        """Abrir la ventana de administración solo si el login es exitoso"""
        dialogo_login = VentanaLogin(self)
        if dialogo_login.ShowModal() == wx.ID_OK:
            self.Hide()
            ventana_admin = VentanaAdmin(self)
            ventana_admin.Show()
        dialogo_login.Destroy()

    def entrar_como_cliente(self, event):
        """
        Abrir la ventana de compras
        y ocultar la ventana principal
        """
        self.Hide()
        ventana_cliente = MenuCompras(self)
        ventana_cliente.Show()

    def salir(self, event):
        """Salir de la aplicación"""
        wx.MessageBox("¡Gracias por probar el sistema!", 
                      "Información", wx.ICON_INFORMATION)
        self.Close()

class Aplicacion(wx.App):
    def OnInit(self):
        ventana = VentanaBienvenida()
        ventana.Show()
        return True


if __name__ == "__main__":
    app = Aplicacion()
    app.MainLoop()
