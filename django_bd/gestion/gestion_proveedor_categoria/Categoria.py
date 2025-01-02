# ventana para la categoría de los productos.
import wx
from gestion.crear_menu_secundario import PanelBase
from gestion.db_connection import Categoria, Producto

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

    def populate_tree(self):
        """Llena el árbol con categorías y productos"""
        root = self.tree_ctrl.AddRoot('Categorías')
        categorias = Categoria.objects.all()
        
        for categoria in categorias:
            cat_item = self.tree_ctrl.AppendItem(root, categoria.nombre)
            productos = Producto.objects.filter(categoria=categoria)
            for producto in productos:
                self.tree_ctrl.AppendItem(cat_item, producto.nombre)
                
        self.tree_ctrl.Expand(root)

    def on_nuevo(self, event):
        # Implementa la lógica para agregar una nueva categoría o producto
        pass
    
    def on_editar(self, event):
        # Implementa la lógica para editar una categoría o producto
        pass
    
    def on_eliminar(self, event):
        # Implementa la lógica para eliminar una categoría o producto
        pass

