import wx
from gestion.agregar_actualiza import Formulario
from gestion.db_connection import Cliente

class ActualizaCliente(Formulario):
    def __init__(self, cliente,actualizar_lista_callback=None):
        super().__init__(None, title="Actualizar Cliente")
        self.actualizar_lista_callback = actualizar_lista_callback  # Callback para actualizar lista

        if not cliente:
            wx.MessageBox("El cliente no es válido o no se ha proporcionado.", "Error", wx.ICON_ERROR)
            self.Close()
            return

        self.cliente = cliente

        # Campo de entrada para la cédula (solo lectura)
        self.cedula_label = wx.StaticText(self.panel, label="Cédula:")
        self.sizer.Insert(0, self.cedula_label, 0, wx.ALL, 5)
        self.cedula_input = wx.TextCtrl(self.panel, value=cliente.cedula, style=wx.TE_READONLY)
        self.sizer.Insert(1, self.cedula_input, 0, wx.EXPAND | wx.ALL, 5)

        # Rellenar campos con los valores actuales
        try:
            self.name_input.SetValue(cliente.nombre or "")
            self.surname_input.SetValue(cliente.apellido or "")
            self.email_input.SetValue(cliente.email or "")
            self.telefono_input.SetValue(cliente.telefono or "")
            self.direccion_input.SetValue(cliente.direccion or "")
        except AttributeError as e:
            wx.MessageBox(f"Error al asignar valores: {e}", "Error", wx.ICON_ERROR)
            self.Close()
            return

        # Agregar botones
        self.agregar_botones(self.guardar, self.cancelar)
        self.Show()

    def guardar(self, event):
        try:
            self.cliente.nombre = self.name_input.GetValue()
            self.cliente.apellido = self.surname_input.GetValue()
            self.cliente.email = self.email_input.GetValue()
            self.cliente.telefono = self.telefono_input.GetValue()
            self.cliente.direccion = self.direccion_input.GetValue()
            self.cliente.save()
            if self.actualizar_lista_callback:
                self.actualizar_lista_callback()
            wx.MessageBox("Cliente actualizado con éxito.", "Éxito", wx.ICON_INFORMATION)
            self.Close()
        except Exception as e:
            wx.MessageBox(f"Error al actualizar el cliente: {e}", "Error", wx.ICON_ERROR)

    def cancelar(self, event):
        self.Close()