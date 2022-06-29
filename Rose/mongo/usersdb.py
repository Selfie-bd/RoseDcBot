from threading import RLock
from time import time
from Rose.mongo import MongoDB

INSERTION_LOCK = RLock()

from Rose.mongo import usersdb

class Users(MongoDB):
    db_name = "users"

    def __init__(self, user_id: int) -> None:
        super().__init__(self.db_name)
        self.user_id = user_id
        self.user_info = self.__ensure_in_db()

    def update_user(self, name: str, username: str = None):
        with INSERTION_LOCK:
            if name != self.user_info["name"] or username != self.user_info["username"]:
                return self.update(
                    {"_id": self.user_id},
                    {"username": username, "name": name},
                )
            return True

    def delete_user(self):
        with INSERTION_LOCK:
            return self.delete_one({"_id": self.user_id})


    def count_users():
        with INSERTION_LOCK:
            collection = MongoDB(Users.db_name)
            return collection.count()

    def get_my_info(self):
        with INSERTION_LOCK:
            return self.user_info

    def list_users():
        with INSERTION_LOCK:
            collection = MongoDB(Users.db_name)
            return collection.find_all()


    def get_user_info(user_id: int or str):
        with INSERTION_LOCK:
            collection = MongoDB(Users.db_name)
            if isinstance(user_id, int):
                curr = collection.find_one({"_id": user_id})
            elif isinstance(user_id, str):
                curr = collection.find_one({"username": user_id[1:]})
            else:
                curr = None

            if curr:
                return curr

            return {}

#users main
async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"bot_users": user_id})
    if not user:
        return False
    return True

async def get_served_users() -> list:
    users = usersdb.find({"bot_users": {"$gt": 0}})
    if not users:
        return []
    users_list = []
    for user in await users.to_list(length=1000000000):
        users_list.append(user)
    return users_list


async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"bot_users": user_id})

async def remove_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersdb.delete_one({"bot_users": user_id})

#--------------------------------------------------------
async def iss_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"bots_users": user_id})
    if not user:
        return False
    return True

async def gets_served_users() -> list:
    users = usersdb.find({"bots_users": {"$gt": 0}})
    if not users:
        return []
    users_list = []
    for user in await users.to_list(length=1000000000):
        users_list.append(user)
    return users_list


async def adds_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"bots_users": user_id})

async def removes_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersdb.delete_one({"bots_users": user_id})