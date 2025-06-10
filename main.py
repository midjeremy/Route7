from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

#importar pantallas
from APP.login import LoginScreen

class MyScreenManager(ScreenManager):
    pass

class MiApp(App):
    def build(self):
        self.title = "Route 7"
        #carga manual de los archivos kv
        from kivy.lang import Builder
        Builder.load_file('template/login.kv')

        sm = MyScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        return sm
    
if __name__ == '__main__':
    MiApp().run()