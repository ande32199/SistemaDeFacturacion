import wx

class FormularioCliente(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(400, 500))
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Campo de entrada para el nombre
        self.name_label = wx.StaticText(self.panel, label="Nombre:")
        self.sizer.Add(self.name_label, 0, wx.ALL, 5)
        self.name_input = wx.TextCtrl(self.panel)
        self.sizer.Add(self.name_input, 0, wx.EXPAND | wx.ALL, 5)

        # Campo de entrada para el apellido
        self.surname_label = wx.StaticText(self.panel, label="Apellido:")
        self.sizer.Add(self.surname_label, 0, wx.ALL, 5)
        self.surname_input = wx.TextCtrl(self.panel)
        self.sizer.Add(self.surname_input, 0, wx.EXPAND | wx.ALL, 5)

        # Campo de entrada para el email
        self.email_label = wx.StaticText(self.panel, label="Email:")
        self.sizer.Add(self.email_label, 0, wx.ALL, 5)
        self.email_input = wx.TextCtrl(self.panel)
        self.sizer.Add(self.email_input, 0, wx.EXPAND | wx.ALL, 5)

        # Campo de entrada para el teléfono
        self.telefono_label = wx.StaticText(self.panel, label="Teléfono:")
        self.sizer.Add(self.telefono_label, 0, wx.ALL, 5)
        self.telefono_input = wx.TextCtrl(self.panel)
        self.sizer.Add(self.telefono_input, 0, wx.EXPAND | wx.ALL, 5)

        # Campo de entrada para la dirección
        self.direccion_label = wx.StaticText(self.panel, label="Dirección:")
        self.sizer.Add(self.direccion_label, 0, wx.ALL, 5)
        self.direccion_input = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        self.sizer.Add(self.direccion_input, 1, wx.EXPAND | wx.ALL, 5)

    def agregar_botones(self, guardar_callback, cancelar_callback=None):
        # Botón para guardar
        self.save_button = wx.Button(self.panel, label="Guardar")
        self.sizer.Add(self.save_button, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.save_button.Bind(wx.EVT_BUTTON, guardar_callback)

        # Botón para cancelar (opcional)
        if cancelar_callback:
            self.cancel_button = wx.Button(self.panel, label="Cancelar")
            self.sizer.Add(self.cancel_button, 0, wx.ALIGN_CENTER | wx.ALL, 10)
            self.cancel_button.Bind(wx.EVT_BUTTON, cancelar_callback)

        self.panel.SetSizer(self.sizer)
