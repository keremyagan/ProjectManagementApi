from pymongo import MongoClient
from ..config import config
from typing import Union

mongo_server = config.mongo.mongo_server

async def connect_to_db() ->MongoClient :
    '''
    Connects to database
    '''
    return MongoClient(mongo_server)
    
    
async def close_db_connection(client:MongoClient)->None :
    '''
    Closes the database connection
    '''
    client.close()
    