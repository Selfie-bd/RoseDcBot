from sys import exit as exiter
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from Rose import DB_URI
from Rose import *
import pymongo

langdb = db.language
chatsdb = db.chats
nexaub_antif = db.nexa_mongodb
antiservicedb = db.antiservice
flooddb = db.flood_toggle
usersdb = db.users
restartdb = db.restart_stage
chatb = db.chatbot
kukib = db.kuki
lunab = db.luna
nightmod =db.nightmode2
taggeddb = db.tagallert
lockdb = db.lockdb1
botlock = db.botlock
afkusers = db.afkusers

myapp = pymongo.MongoClient(MONGO_URL)
dbx = myapp["AsyncIOMotorCursor"]

federation = dbx['federation']
nm = dbx['Nightmode']

try:
    client = MongoClient(DB_URI)
except PyMongoError as f:
    exiter(1)
main_db = client["maindb"]


class MongoDB:

    def __init__(self, collection) -> None:
        self.collection = main_db[collection]

    def insert_one(self, document):
        result = self.collection.insert_one(document)
        return repr(result.inserted_id)

    def find_one(self, query):
        result = self.collection.find_one(query)
        if result:
            return result
        return False

    def find_all(self, query=None):
        if query is None:
            query = {}
        return list(self.collection.find(query))

    def count(self, query=None):
        if query is None:
            query = {}
        return self.collection.count_documents(query)

    def delete_one(self, query):
        self.collection.delete_many(query)
        return self.collection.count_documents({})

    def replace(self, query, new_data):
        old = self.collection.find_one(query)
        _id = old["_id"]
        self.collection.replace_one({"_id": _id}, new_data)
        new = self.collection.find_one({"_id": _id})
        return old, new

    def update(self, query, update):
        result = self.collection.update_one(query, {"$set": update})
        new_document = self.collection.find_one(query)
        return result.modified_count, new_document

    @staticmethod
    def close():
        return client.close()


def __connect_first():
    _ = MongoDB("test")


__connect_first()