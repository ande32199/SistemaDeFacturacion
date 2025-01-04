
    def agregar_al_carrito(self, event):
        """Agregar producto seleccionado al carrito con un ComboBox adicional"""
        selected = self.list_control.GetFirstSelected()
        if selected == -1:
            wx.MessageBox("Seleccione un producto primero.", "Error", wx.ICON_ERROR)
            return
        # Obtener detalles del producto seleccionado
        codigo = self.list_control.GetItemText(selected, 0)
        try:
            # Buscar el objeto Producto en la base de datos
            producto = Producto.objects.get(codigo=codigo)
        except Producto.DoesNotExist:
            wx.MessageBox("El producto no existe en la base de datos.", "Error", wx.ICON_ERROR)
            return
        # Crear un cuadro de diálogo personalizado para ingresar la cantidad y seleccionar opciones
        dlg = wx.Dialog(self, title="Agregar al Carrito", size=(400, 200))
        dlg_sizer = wx.BoxSizer(wx.VERTICAL)
        # Etiqueta y cuadro de texto para ingresar la cantidad
        cantidad_label = wx.StaticText(dlg, label="Cantidad:")
        cantidad_text = wx.TextCtrl(dlg, value="1")  # Por defecto, la cantidad es 1
        dlg_sizer.Add(cantidad_label, 0, wx.ALL, 5)
        dlg_sizer.Add(cantidad_text, 0, wx.EXPAND | wx.ALL, 5)
        # Etiqueta y ComboBox para seleccionar opciones (por ejemplo, tipo de empaquetado)
        combo_label = wx.StaticText(dlg, label="Opciones:")
        combo_box = wx.ComboBox(dlg, choices=["Unidad", "Paquete de 10", "Paquete de 20"], style=wx.CB_READONLY)
        combo_box.SetSelection(0)  # Seleccionar la primera opción por defecto
        dlg_sizer.Add(combo_label, 0, wx.ALL, 5)
        dlg_sizer.Add(combo_box, 0, wx.EXPAND | wx.ALL, 5)
        # Botones para confirmar o cancelar
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_ok = wx.Button(dlg, label="Aceptar")
        btn_cancel = wx.Button(dlg, label="Cancelar")
        btn_sizer.Add(btn_ok, 0, wx.RIGHT, 5)
        btn_sizer.Add(btn_cancel, 0, wx.LEFT, 5)
        dlg_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        dlg.SetSizer(dlg_sizer)
        # Eventos de botones
        btn_ok.Bind(wx.EVT_BUTTON, lambda evt: dlg.EndModal(wx.ID_OK))
        btn_cancel.Bind(wx.EVT_BUTTON, lambda evt: dlg.EndModal(wx.ID_CANCEL))

        # Mostrar el cuadro de diálogo
        if dlg.ShowModal() == wx.ID_OK:
            try:
                cantidad = int(cantidad_text.GetValue())
                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser mayor a cero.")
                if cantidad > producto.stock:
                    wx.MessageBox(f"Stock insuficiente. Solo hay {producto.stock} unidades disponibles.", "Error", wx.ICON_ERROR)
                    dlg.Destroy()
                    return

                # Obtener la opción seleccionada del ComboBox
                opcion_seleccionada = combo_box.GetStringSelection()
                # Calcular el total
                precio = float(producto.precio)
                total = cantidad * precio
                # Agregar el producto al carrito
                self.carrito.append({
                    'producto': producto,  # Agregar el objeto Producto al carrito
                    'codigo': producto.codigo,
                    'nombre': producto.nombre,
                    'cantidad': cantidad,
                    'precio': precio,
                    'total': total,
                    'opcion': opcion_seleccionada  # Guardar la opción seleccionada
                })
                # Actualizar la lista del carrito
                index = self.carrito_list.GetItemCount()
                self.carrito_list.InsertItem(index, producto.codigo)
                self.carrito_list.SetItem(index, 1, producto.nombre)
                self.carrito_list.SetItem(index, 2, str(cantidad))
                self.carrito_list.SetItem(index, 3, f"${precio:.2f}")
                self.carrito_list.SetItem(index, 4, f"${total:.2f}")

                # Hacer visibles los botones y el carrito
                self.btn_quitar.Show()
                self.btn_facturar.Show()
                self.carrito_list.Show()
            except ValueError as e:
                wx.MessageBox(f"Entrada no válida: {e}", "Error", wx.ICON_ERROR)
        dlg.Destroy()


    def generar_factura(self, event):
        if not self.carrito:
            wx.MessageBox('El carrito está vacío', 'Error', wx.OK | wx.ICON_ERROR)
            return

        # Diálogo para seleccionar cliente
        dlg = wx.TextEntryDialog(self, 'Ingrese la cédula del cliente:', 'Cliente')
        if dlg.ShowModal() == wx.ID_OK:
            try:
                cliente = Cliente.objects.get(cedula=dlg.GetValue())
                
                # Crear factura
                factura = Factura.objects.create(cliente=cliente)
                
                # Crear detalles
                for item in self.carrito:
                    DetalleFactura.objects.create(
                        factura=factura,
                        producto=item['producto'],
                        cantidad=item['cantidad']
                    )
                
                # Actualizar stock
                factura.actualizar_stock()
                
                # Limpiar carrito
                self.carrito = []
                self.carrito_list.DeleteAllItems()
                self.actualizar_lista(None)
                self.Layout()
                # generar el pdf con los detalles de la factura.
                self.generar_pdf_factura(factura)
                wx.MessageBox(f'Factura generada con éxito\nTotal: ${factura.total}', 'Éxito', wx.OK | wx.ICON_INFORMATION)
                self.btn_quitar.Hide()
                self.btn_facturar.Hide()
                self.carrito_list.Hide()
                self.Layout()
            except Cliente.DoesNotExist:
                wx.MessageBox('Cliente no encontrado. Agregue el cliente.', 'Error', wx.OK | wx.ICON_ERROR)
                dlg.Destroy()
                # Abrir el formulario para agregar un cliente
                agregar_cliente = AgregarCliente(self.actualizar_lista)
            except Exception as e:
                wx.MessageBox(f'Error al generar la factura: {str(e)}', 'Error', wx.OK | wx.ICON_ERROR)
        dlg.Destroy()

