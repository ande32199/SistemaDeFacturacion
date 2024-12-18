import wx
from facturacion.models import Producto, Categoria, Proveedor

class ProductoDialog(wx.Dialog):
    def __init__(self, parent, title, producto=None):
        super().__init__(parent, title=title, size=(400, 500))
        self.producto = producto
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Campos del formulario
        self.add_text_field("Código:", "codigo")
        self.add_text_field("Nombre:", "nombre")
        self.add_text_field("Precio:", "precio")
        self.add_text_field("Stock:", "stock")
        
        # Combobox para Categoría
        categorias = Categoria.objects.all()
        self.categoria_combo = self.add_combo_field("Categoría:", 
            [(c.id, c.nombre) for c in categorias])
        
        # Combobox para Proveedor
        proveedores = Proveedor.objects.all()
        self.proveedor_combo = self.add_combo_field("Proveedor:", 
            [(p.ruc, p.nombre) for p in proveedores])

        # Botones
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        save_btn = wx.Button(self.panel, label="Guardar")
        cancel_btn = wx.Button(self.panel, label="Cancelar")
        
        btn_sizer.Add(save_btn, 0, wx.ALL, 5)
        btn_sizer.Add(cancel_btn, 0, wx.ALL, 5)
        
        self.sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        # Eventos
        save_btn.Bind(wx.EVT_BUTTON, self.on_save)
        cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)

        # Si es edición, llenar los campos
        if self.producto:
            self.fields['codigo'].SetValue(self.producto.codigo)
            self.fields['codigo'].Disable()
            self.fields['nombre'].SetValue(self.producto.nombre)
            self.fields['precio'].SetValue(str(self.producto.precio))
            self.fields['stock'].SetValue(str(self.producto.stock))
            if self.producto.categoria:
                self.categoria_combo.SetValue(self.producto.categoria.nombre)
            if self.producto.proveedor:
                self.proveedor_combo.SetValue(self.producto.proveedor.nombre)

        self.panel.SetSizer(self.sizer)

    def add_text_field(self, label, name):
        label_ctrl = wx.StaticText(self.panel, label=label)
        self.sizer.Add(label_ctrl, 0, wx.ALL, 5)
        
        text_ctrl = wx.TextCtrl(self.panel)
        self.sizer.Add(text_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        
        if not hasattr(self, 'fields'):
            self.fields = {}
        self.fields[name] = text_ctrl

    def add_combo_field(self, label, choices):
        label_ctrl = wx.StaticText(self.panel, label=label)
        self.sizer.Add(label_ctrl, 0, wx.ALL, 5)
        
        combo = wx.ComboBox(self.panel, choices=[c[1] for c in choices])
        self.sizer.Add(combo, 0, wx.EXPAND | wx.ALL, 5)
        return combo

    def on_save(self, event):
        try:
            # Obtener valores
            codigo = self.fields['codigo'].GetValue()
            nombre = self.fields['nombre'].GetValue()
            precio = float(self.fields['precio'].GetValue())
            stock = int(self.fields['stock'].GetValue())
            
            # Obtener categoría y proveedor seleccionados
            categoria_nombre = self.categoria_combo.GetValue()
            proveedor_nombre = self.proveedor_combo.GetValue()
            
            categoria = Categoria.objects.get(nombre=categoria_nombre) if categoria_nombre else None
            proveedor = Proveedor.objects.get(nombre=proveedor_nombre) if proveedor_nombre else None

            # Crear o actualizar producto
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
            
            self.Close()
            
        except ValueError as e:
            wx.MessageBox("Error en los datos ingresados", "Error", wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(f"Error al guardar: {str(e)}", "Error", wx.ICON_ERROR)

    def on_cancel(self, event):
        self.Close()