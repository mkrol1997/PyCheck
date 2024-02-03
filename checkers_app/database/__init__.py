import os

from pymongo import MongoClient

DB_URI = f"mongodb://{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"

client = MongoClient(DB_URI)
db = client.pycheck
