from pymongo import MongoClient
from Rose import *

MONGO_PORT = ("27017")
MONGO_DB_URI = MONGO_URL
MONGO_DB = "Rose"

anti = MongoClient(MONGO_DB_URI)[MONGO_DB]


anitcdb = anti["ANTICHANNEL"]

async def is_antichnl(group_id):
    data = anitcdb.find_one({"group_id": group_id})
    if not data:
        return False, None
    else: 
        return True, data["mode"]

async def antichnl_on(group_id, mode):
    data = {
        "group_id":group_id,
        "mode":(mode)}
    try:
        anitcdb.update_one({"group_id": group_id},  {"$set": data}, upsert=True)
    except:
        return


def antichnl_off(group_id):
    stark = anitcdb.find_one({"group_id": group_id})
    if not stark:
        return False
    else:
        anitcdb.delete_one({"group_id": group_id})
        return True
