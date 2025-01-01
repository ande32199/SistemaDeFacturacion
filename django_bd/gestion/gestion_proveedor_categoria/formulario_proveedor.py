import wx
from clases_principales.agregar_actualiza import FormularioCliente
from db_connection import Proveedor

class FormularioProveedor(FormularioCliente):
    def __init__(self, parent, proveedor=None, title="Formulario de Proveedor", actualizar_lista_callback=None):
        super().__init__(parent, title)
        self.actualizar_lista_callback = actualizar_lista_callback  # Guardar el callback
        
        # Indica si estamos editando o creando
        self.proveedor_existente = proveedor
        self.modo_edicion = proveedor is not None
        
        # Remover campos no necesarios
        self.email_label.Destroy()
        self.email_input.Destroy()
        self.surname_label.Destroy()
        self.surname_input.Destroy()
        
        # Cambiar etiqueta de "Nombre" por campos específicos de Proveedor
        self.name_label.SetLabel("Razón Social:")
        
        # Añadir campo RUC antes del nombre
        self.sizer.Clear()  # Limpiar el sizer para reorganizar los elementos
        
        # Campo RUC
        self.ruc_label = wx.StaticText(self.panel, label="RUC:")
        self.ruc_input = wx.TextCtrl(self.panel)
        
        # Si estamos en modo edición, hacer RUC de solo lectura
        if self.modo_edicion:
            self.ruc_input.SetEditable(False)
            self.ruc_input.SetBackgroundColour(wx.LIGHT_GREY)
        
        # Reorganizar todos los campos
        self.sizer.Add(self.ruc_label, 0, wx.ALL, 5)
        self.sizer.Add(self.ruc_input, 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.name_label, 0, wx.ALL, 5)
        self.sizer.Add(self.name_input, 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.telefono_label, 0, wx.ALL, 5)
        self.sizer.Add(self.telefono_input, 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.direccion_label, 0, wx.ALL, 5)
        self.sizer.Add(self.direccion_input, 1, wx.EXPAND | wx.ALL, 5)
        
        # Si hay un proveedor existente, cargar sus datos
        if self.proveedor_existente:
            self.cargar_datos_proveedor()
        
        # Ajustar el tamaño del formulario
        self.SetSize((400, 450))
        
        # Método para manejar el guardado
        self.guardar_callback = self.guardar_proveedor
    
    def cargar_datos_proveedor(self):
        """Carga los datos del proveedor existente en el formulario"""
        self.ruc_input.SetValue(self.proveedor_existente.ruc)
        self.name_input.SetValue(self.proveedor_existente.nombre)
        self.telefono_input.SetValue(self.proveedor_existente.telefono or '')
        self.direccion_input.SetValue(self.proveedor_existente.direccion or '')
        
    def guardar_proveedor(self, event):
        """Método para guardar o actualizar el proveedor"""
        if self.validar_datos():
            datos = self.get_datos()
            try:
                if self.modo_edicion:
                    # Actualizar proveedor existente
                    for key, value in datos.items():
                        if key != 'ruc':  # No actualizar el RUC
                            setattr(self.proveedor_existente, key, value)
                    self.proveedor_existente.save()
                    mensaje = "Proveedor actualizado exitosamente"
                else:
                    # Crear nuevo proveedor
                    proveedor = Proveedor(**datos)
                    proveedor.save()
                    mensaje = "Proveedor guardado exitosamente"
                
                wx.MessageBox(mensaje, "Éxito", wx.OK | wx.ICON_INFORMATION)
                if self.actualizar_lista_callback:
                    self.actualizar_lista_callback()  # Llamar al callback para actualizar la lista de proveedores
                self.Close()
            except Exception as e:
                wx.MessageBox(f"Error al guardar: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def get_datos(self):
        """Método para obtener los datos del formulario en formato diccionario"""
        return {
            'ruc': self.ruc_input.GetValue().strip(),
            'nombre': self.name_input.GetValue().strip(),
            'telefono': self.telefono_input.GetValue().strip(),
            'direccion': self.direccion_input.GetValue().strip()
        }
    
    def validar_datos(self):
        """Método para validar los datos del formulario"""
        ruc = self.ruc_input.GetValue().strip()
        nombre = self.name_input.GetValue().strip()
        
        if not ruc:
            wx.MessageBox("El RUC es obligatorio", "Error de validación", wx.OK | wx.ICON_ERROR)
            return False
        
        if len(ruc) != 13 or not ruc.isdigit():
            wx.MessageBox("El RUC debe tener 13 dígitos numéricos", "Error de validación", wx.OK | wx.ICON_ERROR)
            return False
        
        if not nombre:
            wx.MessageBox("La Razón Social es obligatoria", "Error de validación", wx.OK | wx.ICON_ERROR)
            return False
        
        return True

# Ejemplo de uso para editar un proveedor existente:
def editar_proveedor(proveedor_existente):
    app = wx.App()
    formulario = FormularioProveedor(None, proveedor=proveedor_existente, title="Editar Proveedor")
    formulario.agregar_botones(formulario.guardar_proveedor, lambda evt: formulario.Close())
    formulario.Show()
    app.MainLoop()

# Ejemplo de uso para crear un nuevo proveedor:
def nuevo_proveedor():
    app = wx.App()
    formulario = FormularioProveedor(None)
    formulario.agregar_botones(formulario.guardar_proveedor, lambda evt: formulario.Close())
    formulario.Show()
    app.MainLoop()

# Para usar en tu código:
"""
# Para editar un proveedor existente:
proveedor = Proveedor.objects.get(ruc='1234567890123')
editar_proveedor(proveedor)

# Para crear un nuevo proveedor:
nuevo_proveedor()
"""