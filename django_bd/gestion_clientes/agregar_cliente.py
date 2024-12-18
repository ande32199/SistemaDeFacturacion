from clases_principales.agregar_actualiza import FormularioCliente
from db_connection import Cliente
import wx

class AgregarCliente(FormularioCliente):
    def __init__(self, actualizar_lista_callback=None):
        super().__init__(None, title="Agregar Cliente")
        self.actualizar_lista_callback = actualizar_lista_callback  # Callback para actualizar lista

        # Campo de entrada para la cédula
        self.cedula_label = wx.StaticText(self.panel, label="Cédula:")
        self.sizer.Insert(0, self.cedula_label, 0, wx.ALL, 5)
        self.cedula_input = wx.TextCtrl(self.panel)
        self.sizer.Insert(1, self.cedula_input, 0, wx.EXPAND | wx.ALL, 5)

        # Agregar botones
        self.agregar_botones(self.guardar, self.on_cancel)
        self.Show()

    def guardar(self, event):
        cedula = self.cedula_input.GetValue().strip()
        nombre = self.name_input.GetValue().strip()
        apellido = self.surname_input.GetValue().strip()
        email = self.email_input.GetValue().strip()
        telefono = self.telefono_input.GetValue().strip()
        direccion = self.direccion_input.GetValue().strip()

        if not cedula or not nombre or not apellido:
            wx.MessageBox("Los campos Cédula, Nombre y Apellido son obligatorios.", "Error", wx.ICON_ERROR)
            return

        if len(cedula) != 10 or (telefono and len(telefono) != 10):
            wx.MessageBox("La cédula y el teléfono deben tener 10 dígitos.", "Error", wx.ICON_ERROR)
            return

        try:
            Cliente.objects.create(
                cedula=cedula,
                nombre=nombre,
                apellido=apellido,
                email=email if email else None,
                telefono=telefono if telefono else None,
                direccion=direccion if direccion else None,
            )
            wx.MessageBox("Cliente agregado con éxito.", "Éxito", wx.ICON_INFORMATION)
            if self.actualizar_lista_callback:
                self.actualizar_lista_callback()  # Llamar al callback para actualizar la lista
            self.Close()
        except Exception as e:
            wx.MessageBox(f"Error al guardar el cliente: {e}", "Error", wx.ICON_ERROR)

    def on_cancel(self, event):
        self.Close()
