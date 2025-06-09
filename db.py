from pymongo import MongoClient
from dotenv import load_dotenv
import os

<<<<<<< HEAD
def get_db ():
    cliente = MongoClient("mongodb+srv://Rodrigo:Rodrigo.Esobrad2025@cluster0.drz7k.mongodb.net/") #Añadir URL
    return cliente["Route7"] #AÑADIR nombre de base de datos
=======
# Cargar variables del archivo .env
load_dotenv()

def get_db ():
    cliente = MongoClient["url"]
    return cliente["db"]
>>>>>>> ec6608602702be122cda71aa1904fa7aac459d38
