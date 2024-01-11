import os

from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient

DB_URI = f"{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_NAME')}"

client = MongoClient(DB_URI)
db = client.pycheck
