# Proyecto de Facturación en Django

Este proyecto es una aplicación de facturación desarrollada en Django. Incluye funcionalidades para gestionar clientes, productos, proveedores, categorías, gestionar inventario y facturas.
fue desarrollado para un deber en la universidad
## Requisitos

1. Python 3.12.7 que fue la versión con la cual se trabajó en este proyecto
2. MySQL instalado y configurado
3. Django 5.1.4
4. Virtualenv (opcional, pero recomendado)

## Configuración

1. Clona el repositorio:
   ```bash
   git clone https://github.com/agus-romero96/SistemaDeFacturacion.git
   cd SistemaDeFacturacion
2. 
Crea y activa un entorno virtual (opcional, pero recomendado):
en este caso yo lo creé así:
python -m venv entorno
y se crea la carpeta llamada entorno
3.
activar el entorno con el comando .\entorno\Scripts\activate
en caso de error abrir la terminar como administrador y escribir el siguiente comando: Set-ExecutionPolicy RemoteSigned
4. 
Instala las dependencias:
pip install -r requirements.txt
5.
Configura las variables de entorno en un archivo con extención .env (puede estar sin nombre, pero la extención es importante)
este archivo debe estar en la misma ubicación que el archivo settings.py dentro de la carpeta django_bd
el contenido de este archivo es:
DJANGO_SECRET_KEY=tu-clave-secreta
DB_NAME=facturacion
DB_USER=root
DB_PASSWORD=la contraseña que pusiste al instalar mysql
DB_HOST=localhost
DB_PORT=3306
6.
creamos la base de datos llamada facturacion
si lo hacemos desde la consola de mysql el comando sería:
CREATE DATABASE facturacion;
7.
aplicar las migraciones
1.
abrir la consola de vs code o del ID que uses.
2.
navegar al directorio del proyecto: en este caso cd django_bd
3.
aplicar las migraciones con el comando:
python manage.py migrate
8. 
Ejecuta el servidor de desarrollo:
python manage.py runserver
9.
opcionalmente puedes entrar al navegador desde:
http://127.0.0.1:8000.
10.
ejecutar main.py para iniciar el programa