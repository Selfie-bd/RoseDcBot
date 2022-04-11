from threading import RLock
from time import time
from Rose.mongo import MongoDB

INSERTION_LOCK = RLock()


class Reporting(MongoDB):
    db_name = "reporting"

    def __init__(self, chat_id: int) -> None:
        super().__init__(self.db_name)
        self.chat_id = chat_id
        self.chat_info = self.__ensure_in_db()

    def get_chat_type(self):
        return "supergroup" if str(self.chat_id).startswith("-100") else "user"

    def set_settings(self, status: bool = True):
        with INSERTION_LOCK:
            self.chat_info["status"] = status
            return self.update(
                {"_id": self.chat_id},
                {"status": self.chat_info["status"]},
            )

    def get_settings(self):
        with INSERTION_LOCK:
            return self.chat_info["status"]

    @staticmethod
    def load_from_db():
        with INSERTION_LOCK:
            collection = MongoDB(Reporting.db_name)
            return collection.find_all() or []

    def __ensure_in_db(self):
        chat_data = self.find_one({"_id": self.chat_id})
        if not chat_data:
            chat_type = self.get_chat_type()
            new_data = {"_id": self.chat_id, "status": True, "chat_type": chat_type}
            self.insert_one(new_data)
            return new_data
        return chat_data

    def migrate_chat(self, new_chat_id: int):
        old_chat_db = self.find_one({"_id": self.chat_id})
        new_data = old_chat_db.update({"_id": new_chat_id})
        self.insert_one(new_data)
        self.delete_one({"_id": self.chat_id})
