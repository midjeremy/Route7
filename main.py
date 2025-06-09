from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

from APP.login import Login
from APP.admin import AdminScreen
from APP.user import UserScreen

class MyScreenManager(ScreenManager):
    """
    MyScreenManager class that inherits from ScreenManager.
    This class manages the screens in the Kivy application.
    """
    pass

class MyApp(App):
    def build(self):
        Builder.load_file('template/Login.kv')
        Builder.load_file('template/admin.kv')
        Builder.load_file('template/user.kv')

        return MyScreenManager()
    
if __name__ == '__main__':
    MyApp().run()