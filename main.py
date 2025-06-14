from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

#importar pantallas
from APP.login import LoginScreen
from APP.admin import AdminScreen
from APP.mapa import MapScreen
from APP.user import UserScreen

class MyScreenManager(ScreenManager):
    pass

class MiApp(App):
    def build(self):
        self.title = "Route 7"
        #carga manual de los archivos kv
        from kivy.lang import Builder
        Builder.load_file('template/login.kv')
        Builder.load_file('template/admin.kv')
        Builder.load_file('template/map.kv')

        sm = MyScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(AdminScreen(name='admin'))
        sm.add_widget(MapScreen(name='mapa'))
        sm.add_widget(UserScreen(name='user'))
        return sm
    
if __name__ == '__main__':
    MiApp().run()