from kivy.uix.screenmanager import Screen

class AdminScreen(Screen):
    '''
    Se define la pantalla de administrador
    Esta pantalla es la que se muestra al administrador
    y permite gestionar los usuarios, rutas y otros aspectos del sistema.
    Esta pantalla es accesible solo para el administrador
    y requiere autenticación previa.
    Esta pantalla se muestra al administrador una vez que ha iniciado sesión
    y se le permite gestionar el sistema.
    Esta pantalla se define en el archivo admin.kv
    y se carga en la aplicación principal.
    Esta pantalla hereda de la clase Screen de Kivy
    y se utiliza para mostrar la interfaz de usuario del administrador.
    '''

    def desconectar(self):
        '''
        Método para desconectar al administrador
        y volver a la pantalla de inicio de sesión.
        Este método se llama cuando el administrador hace clic en el botón de desconexión.
        '''
        self.manager.current = 'login'

    def ver_mapa(self):
        '''
        Método para ver el mapa
        Este método se llama cuando el administrador hace clic en el botón de ver mapa.
        Redirige a la pantalla del mapa.
        '''
        self.manager.current = 'mapa'

    pass