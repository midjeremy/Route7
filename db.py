from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

def get_db ():
    cliente = MongoClient["url"]
    return cliente["db"]
