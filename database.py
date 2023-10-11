from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo
import os
from dotenv import load_dotenv


def set_up_collection():
    load_dotenv()

    # Set up mongoDB client
    database_url = os.getenv("MONGODB_URI")

    # Create a new client and connect to the server
    client = MongoClient(database_url, server_api=ServerApi('1'))

    db = client["Tetris"]
    collection = db["high-scores"]

    return collection


def return_top_ten_scores():
    collection = set_up_collection()

    top_10_results = collection.find().sort("score", pymongo.DESCENDING).limit(10)

    scores = [int(document["score"]) for document in top_10_results]

    return scores


def insert_new_score(score):
    collection = set_up_collection()

    data = {
        "score": score
    }

    collection.insert_one(data)
