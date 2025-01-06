import wx
from gestion.db_connection import Categoria
from gestion.crear_menu_secundario import PanelBase

class FormularioCategoria(wx.Dialog):
    def __init__(self, parent, title, categoria=None, actualizar_lista_callback=None):
        super().__init__(parent, title=title, size=(400, 300))
        self.categoria = categoria
        self.actualizar_lista_callback = actualizar_lista_callback
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.campos = {}

        # Campos del formulario
        self.agregar_texto("Nombre:", "nombre")
        self.agregar_texto("Descripción:", "descripcion")

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
        if self.categoria:
            self.campos['nombre'].SetValue(str(self.categoria.nombre))
            self.campos['descripcion'].SetValue(str(self.categoria.descripcion))

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

    def al_guardar(self, event):
        try:
            # Obtener y validar los valores
            nombre = self.campos['nombre'].GetValue().strip()
            descripcion = self.campos['descripcion'].GetValue().strip()

            # Validaciones
            if not nombre:
                wx.MessageBox("El nombre es obligatorio", "Error", wx.ICON_ERROR)
                return

            # Guardar o actualizar
            if self.categoria:
                self.categoria.nombre = nombre
                self.categoria.descripcion = descripcion
                self.categoria.save()
            else:
                Categoria.objects.create(
                    nombre=nombre,
                    descripcion=descripcion
                )

            if self.actualizar_lista_callback:
                self.actualizar_lista_callback()

            wx.MessageBox("Categoría guardada exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)

        except Exception as e:
            wx.MessageBox(f"Error al procesar los datos: {str(e)}", "Error", wx.ICON_ERROR)

    def al_cancelar(self, event):
        self.EndModal(wx.ID_CANCEL)

class PanelCategoria(PanelBase):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Lista de categorías
        self.list_control = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.list_control.InsertColumn(0, 'ID', width=50)
        self.list_control.InsertColumn(1, 'Nombre', width=200)
        self.list_control.InsertColumn(2, 'Descripción', width=300)
        
        self.sizer.Add(self.list_control, 1, wx.EXPAND | wx.ALL, 5)
        
        # Vincular eventos
        self.btn_nuevo.Bind(wx.EVT_BUTTON, self.on_nuevo)
        self.btn_editar.Bind(wx.EVT_BUTTON, self.on_editar)
        self.btn_eliminar.Bind(wx.EVT_BUTTON, self.on_eliminar)
        
        self.actualizar_lista()
    
    def actualizar_lista(self):
        """Actualiza la lista de categorías"""
        self.list_control.DeleteAllItems()
        categorias = Categoria.objects.all()
        for categoria in categorias:
            index = self.list_control.InsertItem(self.list_control.GetItemCount(), str(categoria.id))
            self.list_control.SetItem(index, 1, categoria.nombre)
            self.list_control.SetItem(index, 2, categoria.descripcion or "")
    
    def on_nuevo(self, event):
        """Crear una nueva categoría"""
        try:
            formulario = FormularioCategoria(self, title="Nueva Categoría", actualizar_lista_callback=self.actualizar_lista)
            formulario.ShowModal()
        except Exception as e:
            print(f"Error al abrir formulario: {str(e)}")
            wx.MessageBox(f"Error: {str(e)}", "Error", wx.ICON_ERROR)
    
    def on_editar(self, event):
        """Editar una categoría existente"""
        selected = self.list_control.GetFirstSelected()
        if selected >= 0:
            categoria_id = self.list_control.GetItem(selected, 0).GetText()
            categoria = Categoria.objects.get(id=categoria_id)
            formulario = FormularioCategoria(
                self, 
                title="Editar Categoría",
                categoria=categoria, 
                actualizar_lista_callback=self.actualizar_lista
            )
            formulario.ShowModal()
        else:
            wx.MessageBox("Seleccione una categoría", "Error", wx.ICON_ERROR)
    
    def on_eliminar(self, event):
        """Eliminar una categoría"""
        selected = self.list_control.GetFirstSelected()
        if selected >= 0:
            categoria_id = self.list_control.GetItem(selected, 0).GetText()
            if wx.MessageBox("¿Está seguro de eliminar esta categoría?", 
                             "Confirmar eliminación",
                             wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION) == wx.YES:
                categoria = Categoria.objects.get(id=categoria_id)
                categoria.delete()
                self.actualizar_lista()
        else:
            wx.MessageBox("Seleccione una categoría", "Error", wx.ICON_ERROR)
