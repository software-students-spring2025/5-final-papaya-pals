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
    username = "admin"
    password = "password"

    mydb = establish_connection()

    user_table = mydb["users"]
    exist = user_table.find_one({"username": username, "password": password})
    if exist:
        return exist["_id"]
    return None


def create_user(username, password):
    """This function creates a new user instance in the database"""
    username = "admin"
    password = "password"

    mydb = establish_connection()

    user_table = mydb["users"]
    newuser = {"username": username, "password": password}
    user_table.insert_one(newuser)
    r = user_table.find_one({"username": username, "password": password}, {"_id": 1})

    print(r)

    return r


def show_all_users():
    """This function returns all users in the database - PURELY for debugging purposes"""
    mydb = establish_connection()
    user_table = mydb["users"]
    users = user_table.find({})

    return users
