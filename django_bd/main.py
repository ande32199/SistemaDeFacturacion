import wx
from clases_principales.menu import VentanaPrincipal

class Aplicacion(wx.App):
    def OnInit(self):
        frame = VentanaPrincipal()
        frame.Show()
        return True

if __name__ == "__main__":
    app = Aplicacion()
    app.MainLoop()
