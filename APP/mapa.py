from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy_garden.mapview import MapView, MapMarker
from kivy.graphics import Line, Color

class MapScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.puntos = []  # Guarda (lat, lon)
        self.linea = None
        self.rutas_guardadas = {}

    def on_kv_post(self, base_widget):
        self.ids.map_view.bind(on_touch_down=self.on_map_touch)

    def on_map_touch(self, map_view, touch):
        if not map_view.collide_point(*touch.pos):
            return False

        lat, lon = map_view.get_latlon_at(touch.x, touch.y)
        marker = MapMarker(lat=lat, lon=lon)
        map_view.add_widget(marker)

        self.puntos.append((lat, lon))
        self.dibujar_ruta(map_view)
        return True

    def dibujar_ruta(self, map_view):
        if self.linea:
            map_view.canvas.remove(self.linea)

        puntos_dibujo = []
        for lat, lon in self.puntos:
            x, y = map_view.get_window_xy_from(lat, lon, map_view.zoom)
            puntos_dibujo.extend([x, y])

        with map_view.canvas:
            Color(1, 0, 0, 1)
            self.linea = Line(points=puntos_dibujo, width=2)

    def limpiar_ruta(self):
        self.puntos.clear()
        self.ids.map_view.canvas.clear()
        self.linea = None
        self.ids.map_view.children[:] = [
            w for w in self.ids.map_view.children if not isinstance(w, MapMarker)
        ]

    def save_ruta(self):
        if not self.puntos:
            return

        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        input_name = TextInput(hint_text="Nombre de la ruta", multiline=False)
        btn_guardar = Button(text="Guardar")

        popup = Popup(title="Guardar Ruta", content=layout, size_hint=(0.8, 0.4))
        layout.add_widget(input_name)
        layout.add_widget(btn_guardar)

        def guardar(_):
            name_ruta = input_name.text.strip()
            if name_ruta:
                self.rutas_guardadas[name_ruta] = list(self.puntos)
                self.ids.ruta_selector.values = list(self.rutas_guardadas.keys())
                popup.dismiss()

        btn_guardar.bind(on_press=guardar)
        popup.open()

    def cargar_ruta(self, name_ruta):
        if name_ruta not in self.rutas_guardadas:
            return

        self.puntos = list(self.rutas_guardadas[name_ruta])
        self.ids.map_view.canvas.clear()
        self.linea = None
        self.ids.map_view.children[:] = [
            w for w in self.ids.map_view.children if not isinstance(w, MapMarker)
        ]

        for lat, lon in self.puntos:
            marker = MapMarker(lat=lat, lon=lon)
            self.ids.map_view.add_widget(marker)

        self.dibujar_ruta(self.ids.map_view)

    def salir_mapa(self):
        self.manager.current = 'admin'

