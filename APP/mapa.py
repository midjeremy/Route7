from kivy.uix.screenmanager import Screen
from kivy_garden.mapview import MapView, MapMarker
from kivy.graphics import Line, Color

class MapScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.puntos = []
        self.linea = None

    def on_map_touch(self, map_view, touch):
        if not map_view.collide_point(*touch.pos):
            return False
        
        coord = map_view.get_latlon_at(touch.x, touch.y)
        lat, lon = coord

        marker = MapMarker(lat=lat, lon=lon)
        map_view.add_widget(marker)

        self.puntos.append((touch.x, touch.y))

        self.dibujar_ruta(map_view)
        return True
    
    def dibujar_ruta(self, map_view):
        if self.linea:
            map_view.canvas.remove(self.linea)

        with map_view.canvas:
            Color(1,0,0,1)
            self.linea = Line(points=sum(self.puntos, ()), width=2)
        
    def limpiar_ruta(self):
        self.puntos.clear()
        self.ids.map_view.canvas.clear()

        self.ids.map_view.children[:] = [w for w in self.ids.map_view.children if not isinstance(w,MapMarker)]