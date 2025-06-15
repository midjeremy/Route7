from kivy.uix.screenmanager import Screen

class UserScreen(Screen):
    """
    UserScreen class that inherits from Screen.
    This class represents a screen in the Kivy application.
    """

    def desconectar(self):
        '''
        Método para desconectar al administrador
        y volver a la pantalla de inicio de sesión.
        Este método se llama cuando el administrador hace clic en el botón de desconexión.
        '''
        self.manager.current = 'login'
    pass