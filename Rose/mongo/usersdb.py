# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

from threading import RLock
from time import time

from Rose.mongo import MongoDB

INSERTION_LOCK = RLock()


class Users(MongoDB):
    """Class to manage users for bot."""

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
                # user_id[1:] because we don't want the '@' in the username search!
                curr = collection.find_one({"username": user_id[1:]})
            else:
                curr = None

            if curr:
                return curr

            return {}
