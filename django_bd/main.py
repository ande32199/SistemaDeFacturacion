import wx
from clases_principales.menu_admin import VentanaAdmin



class VentanaBienvenida(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Bienvenido al Sistema", size=(500, 300))
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Título
        titulo = wx.StaticText(panel, label="Bienvenido al Sistema de Gestión")
        font = titulo.GetFont()
        font.SetPointSize(18)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        titulo.SetFont(font)
        
        # Botones de opciones
        btn_admin = wx.Button(panel, label="Entrar como Administrador", size=(200, 50))
        btn_cliente = wx.Button(panel, label="Entrar como Cliente", size=(200, 50))
        btn_salir = wx.Button(panel, label="Salir", size=(200, 50))
        # Enlazar eventos
        btn_admin.Bind(wx.EVT_BUTTON, self.entrar_como_admin)
        btn_cliente.Bind(wx.EVT_BUTTON, self.entrar_como_cliente)
        btn_salir.Bind(wx.EVT_BUTTON, self.salir)
        
        # Añadir widgets al sizer
        sizer.Add(titulo, 0, wx.ALL | wx.CENTER, 20)
        sizer.Add(btn_admin, 0, wx.ALL | wx.CENTER, 10)
        sizer.Add(btn_cliente, 0, wx.ALL | wx.CENTER, 10)
        
        panel.SetSizer(sizer)
        self.Centre()

    def entrar_como_admin(self, event):
        """Abrir la ventana de administración"""
        self.Hide()
        ventana_admin = VentanaAdmin(self)
        ventana_admin.Show()

    def entrar_como_cliente(self, event):
        """Mostrar un mensaje indicando que la opción no está implementada"""
        wx.MessageBox("La interfaz de cliente aún no está implementada.", 
                      "Información", wx.ICON_INFORMATION)
    # opción de salir
    def salir(self, event):
        """Salir de la aplicación"""
        wx.MessageBox("¡Gracias por provar el sistema!", 
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
