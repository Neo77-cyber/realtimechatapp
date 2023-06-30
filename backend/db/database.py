from pymongo import MongoClient
from bson import ObjectId




client = MongoClient("mongodb://localhost:27017/")
db = client["realtime_app"]
collection = db["realtimes"]


def convert_objectid_to_str(data):
    if isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    return data