"""This module houses functions necessary to connect and interact with MongoDB"""

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import certifi


def establish_connection():
    """This function connects to the running Mongo database instance."""
    # load environment variables 
    load_dotenv()

    # connect MongoDB
    uri = os.getenv("MONGO_URI")
    client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
    dbnane = os.getenv("MONGO_DBNAME")
    mydb = client[dbnane]

    return mydb


def get_user(username, password):
    """This function finds a user in the data table if it exists"""
    username = "admin"
    password = "password"

    mydb = establish_connection()

    user_table = mydb["users"]
    newuser= {
        "username": username, "password": password
    }
    user_table.insert_one(newuser)
    r =  user_table.find_one({"username": username, "password": password},{"_id":1})

    print(r)

    return r
    


def create_user(username, password):
    """This function creates a new user instance in the database"""
    pass
