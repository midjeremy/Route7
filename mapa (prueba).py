from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.mapview import MapView, MapMarkerPopup


class MapaPrueba(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Crear el mapa centrado en una ubicación (por ejemplo, Ciudad de México)
        mapview = MapView(zoom=10, lat=19.4326, lon=-99.1332)
        self.add_widget(mapview)

        # Agregar un marcador
        marcador = MapMarkerPopup(lat=19.4326, lon=-99.1332)
        mapview.add_widget(marcador)


class MapaApp(App):
    def build(self):
        return MapaPrueba()


if __name__ == '__main__':
    MapaApp().run()
