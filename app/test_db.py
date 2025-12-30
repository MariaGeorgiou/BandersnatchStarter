from pymongo import MongoClient
from os import getenv
from dotenv import load_dotenv
from certifi import where

# Load environment variables from .env
load_dotenv()

# Connect to MongoDB
client = MongoClient(getenv("DB_URL"), tlsCAFile=where())
db = client["MonsterDB"]  # use the same database name as in your .env

# Test the connection by listing collections
collections = db.list_collection_names()
print("Connection successful! Collections:", collections)