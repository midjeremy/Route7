from pymongo import MongoClient
from dotenv import load_dotenv
import os

def get_db():
    mongo_url = os.getenv("MONGO_URL")
    db_name = os.getenv("MONGO_DB")
    
    cliente = MongoClient(mongo_url)
    return cliente[db_name]

def get_db ():
    cliente = MongoClient["url"]
    return cliente["db"]
