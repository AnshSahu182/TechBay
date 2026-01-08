import os 
from pymongo import MongoClient
import mongomock

def get_mongo_client(testing=False):
    if testing :
        client = MongoClient(os.getenv("MongoClient_URI"))
    else:
        client = mongomock.MongoClient()
    return client

def get_database(testing=False):
    client= get_mongo_client(testing)
    db=client["techbay"]
    return db