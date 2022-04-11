from threading import RLock
from Rose.mongo import MongoDB

INSERTION_LOCK = RLock()


class Approve(MongoDB):
    db_name = "approve"
    def __init__(self, chat_id: int) -> None:
        super().__init__(self.db_name)
        self.chat_id = chat_id
        self.chat_info = self.__ensure_in_db()

    def check_approve(self, user_id: int):
        with INSERTION_LOCK:
            return bool(user_id in self.chat_info["users"])

    def add_approve(self, user_id: int, user_name: str):
        with INSERTION_LOCK:
            self.chat_info["users"].append((user_id, user_name))
            if not self.check_approve(user_id):
                return self.update(
                    {"_id": self.chat_id},
                    {"users": self.chat_info["users"]},
                )
            return True

    def remove_approve(self, user_id: int):
        with INSERTION_LOCK:
            if self.check_approve(user_id):
                user_full = next(
                    user for user in self.chat_info["users"] if user[0] == user_id
                )
                self.chat_info["users"].pop(user_full)
                return self.update(
                    {"_id": self.chat_id},
                    {"users": self.chat_info["users"]},
                )
            return True

    def unapprove_all(self):
        with INSERTION_LOCK:
            return self.delete_one(
                {"_id": self.chat_id},
            )

    def list_approved(self):
        with INSERTION_LOCK:
            return self.chat_info["users"]

    def count_approved(self):
        with INSERTION_LOCK:
            return len(self.chat_info["users"])

    def load_from_db(self):
        return self.find_all()

    def __ensure_in_db(self):
        chat_data = self.find_one({"_id": self.chat_id})
        if not chat_data:
            new_data = {"_id": self.chat_id, "users": []}
            self.insert_one(new_data)
            return new_data
        return chat_data
        
    def migrate_chat(self, new_chat_id: int):
        old_chat_db = self.find_one({"_id": self.chat_id})
        new_data = old_chat_db.update({"_id": new_chat_id})
        self.insert_one(new_data)
        self.delete_one({"_id": self.chat_id})

 
