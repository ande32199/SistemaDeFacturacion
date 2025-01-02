import wx
from gestion.crear_menu_secundario import PanelBase
from gestion.db_connection import Proveedor,Categoria,Producto
from gestion.gestion_proveedor_categoria.formulario_proveedor import FormularioProveedor

class PanelProveedor(PanelBase):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Lista de proveedores
        self.list_control = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.list_control.InsertColumn(0, 'RUC', width=100)
        self.list_control.InsertColumn(1, 'Razón Social', width=200)
        self.list_control.InsertColumn(2, 'Teléfono', width=100)
        self.list_control.InsertColumn(3, 'Dirección', width=200)
        
        self.sizer.Add(self.list_control, 1, wx.EXPAND | wx.ALL, 5)
        
        # Vincular eventos
        self.btn_nuevo.Bind(wx.EVT_BUTTON, self.on_nuevo)
        self.btn_editar.Bind(wx.EVT_BUTTON, self.on_editar)
        self.btn_eliminar.Bind(wx.EVT_BUTTON, self.on_eliminar)
        
        self.actualizar_lista()
    
    def actualizar_lista(self):
        """Actualiza la lista de proveedores"""
        self.list_control.DeleteAllItems()
        proveedores = Proveedor.objects.all()
        for proveedor in proveedores:
            index = self.list_control.InsertItem(self.list_control.GetItemCount(), proveedor.ruc)
            self.list_control.SetItem(index, 1, proveedor.nombre)
            self.list_control.SetItem(index, 2, proveedor.telefono or "")
            self.list_control.SetItem(index, 3, proveedor.direccion or "")
    
    def on_nuevo(self, event):
        """Crear un nuevo proveedor"""
        try:
            formulario = FormularioProveedor(self, actualizar_lista_callback=self.actualizar_lista)
            formulario.agregar_botones(formulario.guardar_proveedor, lambda evt: formulario.Close())
            formulario.Show()
        except Exception as e:
            print(f"Error al abrir formulario: {str(e)}")
            wx.MessageBox(f"Error: {str(e)}", "Error", wx.ICON_ERROR)
    
    def on_editar(self, event):
        """Editar un proveedor existente"""
        selected = self.list_control.GetFirstSelected()
        if selected >= 0:
            ruc = self.list_control.GetItem(selected, 0).GetText()
            proveedor = Proveedor.objects.get(ruc=ruc)
            formulario = FormularioProveedor(
            self, 
            proveedor=proveedor, 
            title="Editar Proveedor",
            actualizar_lista_callback=self.actualizar_lista
            )
            formulario.agregar_botones(formulario.guardar_proveedor, lambda evt: formulario.Close())
            formulario.Show()
        else:
            wx.MessageBox("Seleccione un proveedor", "Error", wx.ICON_ERROR)
    
    def on_eliminar(self, event):
        """Eliminar un proveedor"""
        selected = self.list_control.GetFirstSelected()
        if selected >= 0:
            ruc = self.list_control.GetItem(selected, 0).GetText()
            if wx.MessageBox("¿Está seguro de eliminar este proveedor?", 
                             "Confirmar eliminación",
                             wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION) == wx.YES:
                proveedor = Proveedor.objects.get(ruc=ruc)
                proveedor.delete()
                self.actualizar_lista()
        else:
            wx.MessageBox("Seleccione un proveedor", "Error", wx.ICON_ERROR)




class PanelCategoria(PanelBase):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Árbol de categorías y productos
        self.tree_ctrl = wx.TreeCtrl(self, style=wx.TR_DEFAULT_STYLE)
        self.sizer.Add(self.tree_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        
        self.populate_tree()
        
        # Vincular eventos
        self.btn_nuevo.Bind(wx.EVT_BUTTON, self.on_nuevo)
        self.btn_editar.Bind(wx.EVT_BUTTON, self.on_editar)
        self.btn_eliminar.Bind(wx.EVT_BUTTON, self.on_eliminar)
        self.tree_ctrl.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_item_activated)
        self.tree_ctrl.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.on_right_click)

    def populate_tree(self):
        """Llena el árbol con categorías y productos desde la base de datos"""
        self.tree_ctrl.DeleteAllItems()  # Limpia el árbol antes de llenarlo
        root = self.tree_ctrl.AddRoot('Categorías')  # Nodo raíz

        # Obtener categorías desde la base de datos
        categorias = Categoria.objects.all()

        for categoria in categorias:
            # Crear un nodo para cada categoría y asociar su ID como datos
            cat_item = self.tree_ctrl.AppendItem(root, categoria.nombre)
            self.tree_ctrl.SetItemData(cat_item, ('categoria', categoria.id))
            
            # Obtener productos asociados a esta categoría desde la base de datos
            productos = Producto.objects.filter(categoria=categoria)
            for producto in productos:
                prod_item = self.tree_ctrl.AppendItem(cat_item, producto.nombre)
                self.tree_ctrl.SetItemData(prod_item, ('producto', producto.codigo))
        
        self.tree_ctrl.Expand(root)  # Expandir el nodo raíz automáticamente

    def on_nuevo(self, event):
        """Maneja la lógica para agregar una nueva categoría o producto"""
        item = self.tree_ctrl.GetSelection()
        if not item.IsOk():
            wx.MessageBox("Selecciona un nodo para agregar una categoría o producto.", "Error", wx.ICON_ERROR)
            return
        
        data = self.tree_ctrl.GetItemData(item)
        if data and data[0] == 'producto':
            wx.MessageBox("No puedes agregar una categoría o producto aquí.", "Error", wx.ICON_ERROR)
            return

        if data and data[0] == 'categoria':
            categoria_id = data[1]
            wx.MessageBox(f"Agregar producto a la categoría con ID {categoria_id}.", "Información")
        else:
            wx.MessageBox("Agregar una nueva categoría.", "Información")

    def on_editar(self, event):
        """Maneja la lógica para editar una categoría o producto"""
        item = self.tree_ctrl.GetSelection()
        if not item.IsOk():
            wx.MessageBox("Selecciona un elemento para editar.", "Error", wx.ICON_ERROR)
            return
        
        data = self.tree_ctrl.GetItemData(item)
        if data:
            tipo, id = data
            if tipo == 'categoria':
                wx.MessageBox(f"Editar categoría con ID {id}.", "Información")
            elif tipo == 'producto':
                wx.MessageBox(f"Editar producto con código {id}.", "Información")

    def on_eliminar(self, event):
        """Maneja la lógica para eliminar una categoría o producto"""
        item = self.tree_ctrl.GetSelection()
        if not item.IsOk():
            wx.MessageBox("Selecciona un elemento para eliminar.", "Error", wx.ICON_ERROR)
            return
        
        data = self.tree_ctrl.GetItemData(item)
        if data:
            tipo, id = data
            if tipo == 'categoria':
                wx.MessageBox(f"Eliminar categoría con ID {id}.", "Información")
            elif tipo == 'producto':
                wx.MessageBox(f"Eliminar producto con código {id}.", "Información")

    def on_item_activated(self, event):
        """Maneja la activación de un ítem del árbol"""
        item = event.GetItem()
        if not item.IsOk():
            return
        
        data = self.tree_ctrl.GetItemData(item)
        if data:
            tipo, id = data
            if tipo == 'categoria':
                wx.MessageBox(f"Seleccionaste la categoría con ID {id}.", "Información")
            elif tipo == 'producto':
                wx.MessageBox(f"Seleccionaste el producto con código {id}.", "Información")

    def on_right_click(self, event):
        """Maneja el clic derecho en un ítem del árbol"""
        item = event.GetItem()
        if not item.IsOk():
            return
        
        self.tree_ctrl.SelectItem(item)
        data = self.tree_ctrl.GetItemData(item)
        menu = wx.Menu()
        
        if data and data[0] == 'categoria':
            menu.Append(wx.ID_ADD, "Agregar Producto")
            menu.Append(wx.ID_EDIT, "Editar Categoría")
            menu.Append(wx.ID_DELETE, "Eliminar Categoría")
        elif data and data[0] == 'producto':
            menu.Append(wx.ID_EDIT, "Editar Producto")
            menu.Append(wx.ID_DELETE, "Eliminar Producto")
        else:
            menu.Append(wx.ID_ADD, "Agregar Categoría")
        
        self.PopupMenu(menu)
        menu.Destroy()

