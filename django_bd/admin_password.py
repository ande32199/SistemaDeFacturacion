import os
import django
from django.contrib.auth.hashers import make_password
from gestion.db_connection import AdminPassword


def crear_admin():
    """Función para crear un usuario administrador."""
    username = input("Ingrese el nombre de usuario: ")
    password = input("Ingrese la contraseña: ")

    try:
        # Crear usuario administrador
        admin = AdminPassword(username=username, password=make_password(password))
        admin.save()
        print(f"Usuario administrador '{username}' creado con éxito.")
    except Exception as e:
        print(f"Error al crear el usuario administrador: {e}")

if __name__ == "__main__":
    crear_admin()
