from kivy.uix.screenmanager import Screen
from db import get_db

# Obtener la colección de usuarios
db = get_db()
coleccion = db["Usuario_Camionero"]

class LoginScreen(Screen):

    def verificar_credenciales(self, rut, contrasena):
        if not self.validar_rut(rut):
            self.ids.mensaje_error.text = "RUT inválido"
            return

        if contrasena == "":
            self.ids.mensaje_error.text = "Debe ingresar la contraseña"
            return

        # Simulación de validación (reemplazar con lógica real/API)
        if rut == "12.345.678-9" and contrasena == "1234":
            self.ids.mensaje_error.text = ""
            self.manager.current = "pantalla1"
        else:
            self.ids.mensaje_error.text = "Credenciales incorrectas"

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

        return dv == str(digito_real)
