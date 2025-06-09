from pymongo import MongoClient

def get_db ():
    cliente = MongoClient("mongodb+srv://Rodrigo:Rodrigo.Esobrad2025@cluster0.drz7k.mongodb.net/") #Añadir URL
    return cliente["Route7"] #AÑADIR nombre de base de datos
