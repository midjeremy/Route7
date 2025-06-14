from kivy.uix.screenmanager import Screen
from db import get_db
import os

# Conexión a MongoDB
db = get_db()
coleccion_UC = db["Usuario_Camionero"]
coleccion_UA = db["Usuario_Admin"]


class LoginScreen(Screen):

    def verificar_credenciales(self, rut, contrasena):
        rut = rut.replace(".", "").replace(" ", "").upper()

        if not self.validar_rut(rut):
            self.ids.mensaje_error.text = "RUT inválido"
            return

        if contrasena == "":
            self.ids.mensaje_error.text = "Debe ingresar la contraseña"
            return
        verificar = self.verificar_type_user(rut, contrasena)

    '''
    Verifica el tipo de usuario y redirige a la pantalla correspondiente
    Si el usuario es camionero, se redirige a "mapa"
    Si el usuario es administrador, se redirige a "admin"
    Si las credenciales son incorrectas, se muestra un mensaje de error
    Si el usuario no existe, se muestra un mensaje de error
    Args:
        rut (str): RUT del usuario
        contrasena (str): Contraseña del usuario
    '''

    def verificar_type_user(self, rut, contrasena):
        usuario = coleccion_UC.find_one({"rut": rut})
        if usuario:
            if usuario.get("contrasena") == contrasena:
                self.ids.mensaje_error.text = ""
                self.manager.current = "user"
                os.system('cls')
                print(f'{usuario.get('rut')} || {usuario.get('contrasena')}')
            else:
                self.ids.mensaje_error.text = "Contraseña incorrecta"
        
        usuario = coleccion_UA.find_one({"rut": rut})
        if usuario:
            if usuario.get("contrasena") == contrasena:
                self.ids.mensaje_error.text = ""
                self.manager.current = "admin"
                os.system('cls')
                print(f'{usuario.get("rut")} || {usuario.get("contrasena")}')
            else:
                self.ids.mensaje_error.text = "Contraseña incorrecta"
        else:
            self.ids.mensaje_error.text = "Usuario no encontrado"

            

    '''
    Validador de RUT chileno
    con ultimo digito verificador
    datos recibidos como string
    Ejemplo: 12345678-9 o 12345678-k
    Retorna True si el RUT es válido, False en caso contrario.
    '''

    def validar_rut(self, rut):
        rut = rut.replace(".", "").replace("-", "")

        dv = rut[-1]
        rut = rut[:-1]

        rut = list(rut)
        rut.reverse()

        factores= [2, 3, 4, 5, 6, 7, 2, 3]
        suma = 0
        for indice, digito in enumerate(rut):
            factor = factores[indice]
            resultado = factor * int(digito)
            suma += resultado

        division = int(suma / 11)
        multiplicacion = division * 11

        resta = suma - multiplicacion

        digito_real = 11-resta

        if digito_real == 10:
            digito_real = "k"
        elif digito_real == 11:
            digito_real = 0

        return dv == str(digito_real).lower()
