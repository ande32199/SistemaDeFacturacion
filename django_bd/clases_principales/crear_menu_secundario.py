import wx

class PanelBase(wx.Panel):
    """Panel base para heredar funcionalidad común"""
    def __init__(self, parent):
        super().__init__(parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Barra de herramientas
        self.toolbar = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_nuevo = wx.Button(self, label="&Nuevo")
        self.btn_editar = wx.Button(self, label="&Editar")
        self.btn_eliminar = wx.Button(self, label="Elimina&r")
        
        self.toolbar.Add(self.btn_nuevo, 0, wx.ALL, 5)
        self.toolbar.Add(self.btn_editar, 0, wx.ALL, 5)
        self.toolbar.Add(self.btn_eliminar, 0, wx.ALL, 5)
        
        self.sizer.Add(self.toolbar, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.sizer)