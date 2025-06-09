from pymongo import MongoClient

def get_db ():
    cliente = MongoClient["url"]
    return cliente["db"]
