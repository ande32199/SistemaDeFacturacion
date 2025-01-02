```markdown
# Proyecto de Facturación en Django

Este proyecto es una aplicación de facturación desarrollada en Django. Permite gestionar clientes, productos, proveedores, categorías, inventario y facturas. Fue desarrollado como parte de un deber universitario.

## Requisitos

Para ejecutar este proyecto, asegúrate de tener instaladas las siguientes herramientas y configuraciones:

- **Python 3.12.7** (la versión utilizada para este proyecto)
- **MySQL** instalado y configurado
- **Django 5.1.4**
- **Virtualenv** (opcional, pero recomendado)

---

## Configuración e instalación

### 1. Clonar el repositorio
Primero, clona este repositorio en tu máquina local y accede al directorio del proyecto:
```bash
git clone https://github.com/agus-romero96/SistemaDeFacturacion.git
cd SistemaDeFacturacion
```

---

### 2. Crear y activar un entorno virtual
Se recomienda usar un entorno virtual para mantener las dependencias del proyecto aisladas. Sigue estos pasos:

1. **Crear el entorno virtual**:
   ```bash
   python -m venv entorno
   ```
   Esto creará una carpeta llamada `entorno`.

2. **Activar el entorno virtual**:
   ```bash
   .\entorno\Scripts\activate
   ```
   Si aparece un error, abre la terminal como administrador y ejecuta:
   ```bash
   Set-ExecutionPolicy RemoteSigned
   ```

---

### 3. Instalar las dependencias
Con el entorno virtual activado, instala todas las dependencias necesarias:
```bash
pip install -r requirements.txt
```

---

### 4. Configurar las variables de entorno
Crea un archivo `.env` en la misma ubicación que el archivo `settings.py` dentro de la carpeta `django_bd`. Este archivo debe contener lo siguiente:

```plaintext
DJANGO_SECRET_KEY=tu-clave-secreta
DB_NAME=facturacion
DB_USER=root
DB_PASSWORD=tu-contraseña-de-mysql
DB_HOST=localhost
DB_PORT=3306
```

> **Nota:** La extensión del archivo `.env` es importante.

---

### 5. Crear la base de datos
Desde la consola de MySQL, crea una base de datos llamada `facturacion`:
```sql
CREATE DATABASE facturacion;
```

---

### 6. Aplicar las migraciones
1. Abre la consola en el directorio raíz del proyecto.
2. Navega al directorio donde se encuentra el archivo `manage.py`:
   ```bash
   cd django_bd
   ```
3. Aplica las migraciones de la base de datos:
   ```bash
   python manage.py migrate
   ```

---

### 7. Ejecutar el servidor de desarrollo
Inicia el servidor de desarrollo de Django:
```bash
python manage.py runserver
```
Luego, accede al navegador en la dirección: [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

### 8. Ejecutar el programa principal
Finalmente, ejecuta el programa principal para iniciar la aplicación:
```bash
python main.py
```

---

## Funcionalidades principales

- Gestión de **clientes**, **productos**, **proveedores** y **categorías**.
- Creación y administración de **facturas detalladas**.
- Generación automática de **PDFs** de las facturas.
- Actualización dinámica de inventarios.

---

## Contacto

Si tienes preguntas o sugerencias, contáctame:

- GitHub: [@agus-romero96](https://github.com/agus-romero96)
```

