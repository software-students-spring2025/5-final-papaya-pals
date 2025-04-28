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
    """ uri = os.getenv("MONGO_URI")
    client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
    dbnane = os.getenv("MONGO_DBNAME")
    mydb = client[dbnane] """

    cxn = MongoClient(os.getenv("MONGO_URI"))
    db = cxn[os.getenv("MONGO_DBNAME")]

    
    try:
        cxn.admin.command("ping")
        print(" *", "Connected to MongoDB!")
    except Exception as e:
        print(" * MongoDB connection error:", e)

    return db


def get_user(username, password):
    """This function finds a user in the data table if it exists"""
    username = "admin"
    password = "password"

    mydb = establish_connection()

    user_table = mydb["users"]
    exist= user_table.find_one({"username":username,"password":password})
    if exist:
        return exist["_id"]
    else:
        return None


def create_user(username, password):
    """This function creates a new user instance in the database"""
    username = "admin"
    password = "password"

    mydb = establish_connection()

    user_table = mydb["users"]
    newuser = {
        "username": username, "password": password
    }
    user_table.insert_one(newuser)
    r =  user_table.find_one({"username": username, "password": password},{"_id":1})

    print(r)

    return r


def show_all_users():
    mydb = establish_connection()
    user_table = mydb["users"]
    users = user_table.find({})

    return users