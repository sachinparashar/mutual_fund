import pymongo

def get_connection():
    mongo = pymongo.MongoClient(
        host='localhost',
        port=27017,
        serverSelectionTimeoutMS=1000
    )
    db = mongo.mutual_fund
    return db

