import json
import os
from pymongo import MongoClient  # Importación de pymongo
from APP.db import get_db  # Asumiendo que esta función retorna un objeto MongoClient o una base de datos

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
        self.puntos = []
        self.linea = None
        self.rutas_guardadas = {}
        self.marcadores = []
        self.modo_edicion = False


    def on_kv_post(self, base_widget):
        self.ids.map_view.bind(on_touch_down=self.on_map_touch)
        self.ids.map_view.bind(on_map_relocated=self.redibujar_ruta)
        self.cargar_rutas_desde_db()


    def on_map_touch(self, map_view, touch):
        if not map_view.collide_point(*touch.pos):
            return False

        # Si el modo edición no está activado, dejamos pasar el evento
        if not self.modo_edicion:
            return False  # Así el mapa puede moverse normalmente

        # Si el modo edición está activo, agregamos el punto
        lat, lon = map_view.get_latlon_at(touch.x, touch.y)
        marker = MapMarker(lat=lat, lon=lon)
        map_view.add_widget(marker)
        self.marcadores.append(marker)

        self.puntos.append((lat, lon))
        self.dibujar_ruta(map_view)

        # Desactivamos el modo edición después de agregar
        self.modo_edicion = False

        return True  # Solo consumimos el evento cuando estamos en modo edición


    def dibujar_ruta(self, map_view):
        if self.linea:
            try:
                map_view.canvas.remove(self.linea)
            except Exception as e:
                print(f"Error al eliminar la línea: {e}")

        puntos_dibujo = []
        for lat, lon in self.puntos:
            x, y = map_view.get_window_xy_from(lat, lon, map_view.zoom)
            puntos_dibujo.extend([x, y])

        with map_view.canvas:
            Color(1, 0, 0, 1)
            self.linea = Line(points=puntos_dibujo, width=2)


    def limpiar_ruta(self):
        self.puntos.clear()

        if self.linea:
            try:
                self.ids.map_view.canvas.remove(self.linea)
            except Exception as e:
                print(f"Error al eliminar la línea: {e}")
            self.linea = None

            map_view = self.ids.map_view
            for marker in self.marcadores:
                map_view.remove_widget(marker)
            self.marcadores.clear()

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

                # Guardamos como JSON
                filename = self.guardar_ruta_en_json(name_ruta)

                # Guardamos en MongoDB
                self.guardar_en_base_de_datos(filename)

                # Eliminamos el archivo JSON
                self.eliminar_json(filename)

                popup.dismiss()

        btn_guardar.bind(on_press=guardar)
        popup.open()

    def guardar_ruta_en_json(self, nombre_ruta):
        ruta_json = {
            "nombre_ruta": nombre_ruta,
            "coordenadas": [{"lat": lat, "lon": lon} for lat, lon in self.puntos]
        }

        filename = f"{nombre_ruta.replace(' ', '_')}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(ruta_json, f, ensure_ascii=False, indent=4)

        print(f"Ruta guardada en {filename}")
        return filename

    def guardar_en_base_de_datos(self, filename):
        try:
            db = get_db()  # Obtenemos la base de datos
            rutas_collection = db['Rutas_Camiones']  # Llamamos a la colección 'rutas'

            with open(filename, 'r', encoding='utf-8') as f:
                ruta_data = json.load(f)

            rutas_collection.insert_one(ruta_data)

            print(f"Ruta '{ruta_data['nombre_ruta']}' guardada en MongoDB con éxito")
        except Exception as e:
            print(f"Error al guardar en MongoDB: {e}")

    def cargar_rutas_desde_db(self):
        try:
            db = get_db()
            rutas_collection = db['Rutas_Camiones']
            rutas = rutas_collection.find()  # Traemos todas las rutas

            self.rutas_guardadas.clear()
            for ruta in rutas:
                nombre = ruta.get('nombre_ruta')
                coordenadas = ruta.get('coordenadas', [])
                puntos = [(coord['lat'], coord['lon']) for coord in coordenadas]
                if nombre:
                    self.rutas_guardadas[nombre] = puntos
            
            # Actualizamos el Spinner con los nombres de ruta
            self.ids.ruta_selector.values = list(self.rutas_guardadas.keys())
        except Exception as e:
            print(f"Error al cargar rutas desde MongoDB: {e}")


    def eliminar_json(self, filename):
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Archivo {filename} eliminado correctamente")
        else:
            print(f"El archivo {filename} no existe")

    def cargar_ruta(self, name_ruta):
        print(f"Intentando cargar la ruta: {name_ruta}")
        print(f"Rutas disponibles: {list(self.rutas_guardadas.keys())}")

        if name_ruta not in self.rutas_guardadas:
            print("Ruta no encontrada en rutas_guardadas.")
            return

        self.puntos = list(self.rutas_guardadas[name_ruta])
        # Limpiar ruta anterior (línea y marcadores)
        if self.linea:
            try:
                self.ids.map_view.canvas.remove(self.linea)
            except Exception as e:
                print(f"Error al eliminar la línea: {e}")
            self.linea = None

        map_view = self.ids.map_view
        for marker in self.marcadores:
            map_view.remove_widget(marker)
        self.marcadores.clear()

        # Agregar marcadores para la nueva ruta
        for lat, lon in self.puntos:
            marker = MapMarker(lat=lat, lon=lon)
            map_view.add_widget(marker)
            self.marcadores.append(marker)

        self.dibujar_ruta(map_view)


    def activar_modo_edicion(self):
        self.modo_edicion = True
        print("Modo edición activado")

    def redibujar_ruta(self, *args):
        if not self.puntos:
            return
        self.dibujar_ruta(self.ids.map_view)

    
    def salir_mapa(self):
        self.manager.current = 'admin'