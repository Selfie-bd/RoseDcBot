from threading import RLock
from time import time
from Rose.mongo import MongoDB

INSERTION_LOCK = RLock()


class Rules(MongoDB):
    db_name = "rules"

    def __init__(self, chat_id: int) -> None:
        super().__init__(self.db_name)
        self.chat_id = chat_id
        self.chat_info = self.__ensure_in_db()

    def get_rules(self):
        with INSERTION_LOCK:
            return self.chat_info["rules"]

    def set_rules(self, rules: str):
        with INSERTION_LOCK:
            self.chat_info["rules"] = rules
            self.update({"_id": self.chat_id}, {"rules": rules})

    def get_privrules(self):
        with INSERTION_LOCK:
            return self.chat_info["privrules"]

    def set_privrules(self, privrules: bool):
        with INSERTION_LOCK:
            self.chat_info["privrules"] = privrules
            self.update({"_id": self.chat_id}, {"privrules": privrules})

    def clear_rules(self):
        with INSERTION_LOCK:
            return self.delete_one({"_id": self.chat_id})

    @staticmethod
    def count_chats_with_rules():
        with INSERTION_LOCK:
            collection = MongoDB(Rules.db_name)
            return collection.count({"rules": {"$regex": ".*"}})

    @staticmethod
    def count_privrules_chats():
        with INSERTION_LOCK:
            collection = MongoDB(Rules.db_name)
            return collection.count({"privrules": True})

    @staticmethod
    def count_grouprules_chats():
        with INSERTION_LOCK:
            collection = MongoDB(Rules.db_name)
            return collection.count({"privrules": False})

    @staticmethod
    def load_from_db():
        with INSERTION_LOCK:
            collection = MongoDB(Rules.db_name)
            return collection.find_all()

    def __ensure_in_db(self):
        chat_data = self.find_one({"_id": self.chat_id})
        if not chat_data:
            new_data = {"_id": self.chat_id, "privrules": False, "rules": ""}
            self.insert_one(new_data)
            return new_data
        return chat_data
