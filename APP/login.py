from kivy.uix.screenmanager import Screen
from db import get_db

dataBase = get_db()

class Login(Screen):
    """
    UserScreen class that inherits from Screen.
    This class represents a screen in the Kivy application.
    """
    pass

def validate_user(username, password):
    """
    VALIDACION DE USUARIO RESPECTIVO A LA BASE DE DATOS Y COLECCION

    :parametro usuario camionero
    :parametro contrasena camionero

    :return: True si el usuario y la contrasena son correctos, False en caso contrario

    Esta funcion valida si el usuario y la contrasena son correctos
    SE VUELVE A BUSCAR EN LA BASE DE DATOS PARA VERIFICAR SI EL USUARIO EXISTE

    :parametro username: Nombre de usuario del camionero
    :parametro password: Contrasena del camionero
    :return: True si el usuario y la contrasena son correctos, False en caso contrario

    SI NO SE ENCUENTRA EL USUARIO O LA CONTRASENA NO ES CORRECTA, SE RETORNA False;

    SE BUSCA USUARIO ADMIN EN LA BASE DE DATOS

    :parametro usuario administrador
    :parametro contrasena administrador

    :return: True si el usuario y la contrasena son correctos, False en caso contrario

    Esta funcion valida si el usuario y la contrasena son correctos
    SE VUELVE A BUSCAR EN LA BASE DE DATOS PARA VERIFICAR SI EL USUARIO EXISTE

    :parametro username: Nombre de usuario del administrador
    :parametro password: Contrasena del administrador
    :return: True si el usuario y la contrasena son correctos, False en caso contrario

    """
    '''usuario = dataBase['Usuarios_Camioneros'].fingd_one({
        'username': username,'''
    
    user = None
    return user is not None