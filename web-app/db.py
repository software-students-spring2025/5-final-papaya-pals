"""This module houses functions necessary to connect and interact with MongoDB"""

import os
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv


def establish_connection():
    """This function connects to the running Mongo database instance."""
    # load environment variables
    load_dotenv()

    # connect MongoDB
    cxn = MongoClient(os.getenv("MONGO_URI"))
    db = cxn[os.getenv("MONGO_DBNAME")]

    try:
        cxn.admin.command("ping")
        print(" *", "Connected to MongoDB!")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(" * MongoDB connection error:", e)

    return db


def get_user(username, password):
    """This function finds a user in the data table if it exists"""
    mydb = establish_connection()

    user_table = mydb["users"]
    exist = user_table.find_one({"username": username, "password": password})
    if exist:
        return exist["_id"]
    return None


def create_user(username, password):
    """This function creates a new user instance in the database"""
    mydb = establish_connection()

    user_table = mydb["users"]
    newuser = {
        "username": username,
        "password": password,
        "bankroll": 1000,  # starting bankroll
        "shame_counter": 0  # starting shame counter (always 0)
    }
    user_table.insert_one(newuser)
    r = user_table.find_one({"username": username, "password": password}, {"_id": 1})

    print(r)

    return r

def get_user_data(username):
    """Fetch bankroll and shame counter for a given user"""
    mydb = establish_connection()
    user_table = mydb["users"]
    user = user_table.find_one({"username": username})
    if user:
        return {"bankroll": user.get("bankroll", 0), "shame_counter": user.get("shame_counter", 0)}
    return None

    
def update_user_data(username, bankroll, shame_counter):
    """Update bankroll and shame counter for a user"""
    mydb = establish_connection()
    user_table = mydb["users"]
    user_table.update_one(
        {"username": username},
        {"$set": {"bankroll": bankroll, "shame_counter": shame_counter}}
    )



def show_all_users():
    """This function returns all users in the database - PURELY for debugging purposes"""
    mydb = establish_connection()
    user_table = mydb["users"]
    users = user_table.find({})

    return users
