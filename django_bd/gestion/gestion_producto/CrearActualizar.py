import wx
from gestion.db_connection import Producto, Proveedor, Categoria

class FormularioProducto(wx.Dialog):
    def __init__(self, parent, title, producto=None, actualizar_lista_callback=None):
        super().__init__(parent, title=title, size=(400, 500))
        self.producto = producto
        self.actualizar_lista_callback = actualizar_lista_callback
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.campos = {}  # Inicializar el diccionario de campos

        # Campos del formulario
        self.agregar_texto("Código:", "codigo")
        self.agregar_texto("Nombre:", "nombre")
        self.agregar_texto("Precio:", "precio")
        self.agregar_texto("Stock:", "stock")

        # Combobox para Categoría
        self.agregar_combo("Categoría:", "categoria",
                           [(c.id, c.nombre) for c in Categoria.objects.all()])

        # Combobox para Proveedor
        self.agregar_combo("Proveedor:", "proveedor",
                           [(p.ruc, p.nombre) for p in Proveedor.objects.all()])

        # Botones
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_guardar = wx.Button(self.panel, label="Guardar")
        self.btn_cancelar = wx.Button(self.panel, label="Cancelar")

        btn_sizer.Add(self.btn_guardar, 0, wx.ALL, 5)
        btn_sizer.Add(self.btn_cancelar, 0, wx.ALL, 5)

        self.sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        # Eventos
        self.btn_guardar.Bind(wx.EVT_BUTTON, self.al_guardar)
        self.btn_cancelar.Bind(wx.EVT_BUTTON, self.al_cancelar)

        # Si es edición, llenar los campos
        if self.producto:
            self.campos['codigo'].SetValue(str(self.producto.codigo))
            self.campos['codigo'].Disable()
            self.campos['nombre'].SetValue(str(self.producto.nombre))
            self.campos['precio'].SetValue(str(self.producto.precio))
            self.campos['stock'].SetValue(str(self.producto.stock))
            if self.producto.categoria:
                self.campos['categoria'].SetValue(self.producto.categoria.nombre)
            if self.producto.proveedor:
                self.campos['proveedor'].SetValue(self.producto.proveedor.nombre)

        self.panel.SetSizer(self.sizer)
        self.panel.Layout()
        self.Center()

    def agregar_texto(self, etiqueta, nombre):
        """Método para agregar campos de texto al formulario"""
        etiqueta_ctrl = wx.StaticText(self.panel, label=etiqueta)
        self.sizer.Add(etiqueta_ctrl, 0, wx.ALL, 5)

        text_ctrl = wx.TextCtrl(self.panel)
        self.sizer.Add(text_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        self.campos[nombre] = text_ctrl

    def agregar_combo(self, etiqueta, nombre, opciones):
        """Método para agregar campos combo al formulario"""
        etiqueta_ctrl = wx.StaticText(self.panel, label=etiqueta)
        self.sizer.Add(etiqueta_ctrl, 0, wx.ALL, 5)

        combo = wx.ComboBox(self.panel, choices=[opcion[1] for opcion in opciones], style=wx.CB_READONLY)
        self.sizer.Add(combo, 0, wx.EXPAND | wx.ALL, 5)

        self.campos[nombre] = combo

    def al_guardar(self, event):
        try:
            # Obtener y validar los valores
            codigo = self.campos['codigo'].GetValue().strip()
            nombre = self.campos['nombre'].GetValue().strip()
            precio_str = self.campos['precio'].GetValue().strip()
            stock_str = self.campos['stock'].GetValue().strip()
            categoria_nombre = self.campos['categoria'].GetValue()
            proveedor_nombre = self.campos['proveedor'].GetValue()

            # Validaciones
            if not codigo or not nombre:
                wx.MessageBox("Código y nombre son obligatorios", "Error", wx.ICON_ERROR)
                return

            try:
                precio = float(precio_str) if precio_str else 0
                stock = int(stock_str) if stock_str else 0
            except ValueError:
                wx.MessageBox("Precio y stock deben ser números válidos", "Error", wx.ICON_ERROR)
                return

            # Obtener objetos de categoría y proveedor
            categoria = Categoria.objects.get(nombre=categoria_nombre) if categoria_nombre else None
            proveedor = Proveedor.objects.get(nombre=proveedor_nombre) if proveedor_nombre else None

            # Guardar o actualizar
            if self.producto:
                self.producto.nombre = nombre
                self.producto.precio = precio
                self.producto.stock = stock
                self.producto.categoria = categoria
                self.producto.proveedor = proveedor
                self.producto.save()
            else:
                Producto.objects.create(
                    codigo=codigo,
                    nombre=nombre,
                    precio=precio,
                    stock=stock,
                    categoria=categoria,
                    proveedor=proveedor
                )

            if self.actualizar_lista_callback:
                self.actualizar_lista_callback()

            wx.MessageBox("Producto guardado exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)

        except Exception as e:
            wx.MessageBox(f"Error al procesar los datos: {str(e)}", "Error", wx.ICON_ERROR)

    def al_cancelar(self, event):
        self.EndModal(wx.ID_CANCEL)
