from threading import RLock
from time import time

from Rose.mongo import MongoDB

INSERTION_LOCK = RLock()


class Warns(MongoDB):
    db_name = "chat_warns"

    def __init__(self, chat_id: int) -> None:
        super().__init__(self.db_name)
        self.chat_id = chat_id

    def warn_user(self, user_id: int, warn_reason=None):
        with INSERTION_LOCK:
            self.user_info = self.__ensure_in_db(user_id)
            self.user_info["warns"].append(warn_reason)
            self.user_info["num_warns"] = len(self.user_info["warns"])
            self.update(
                {"chat_id": self.chat_id, "user_id": user_id},
                {
                    "warns": self.user_info["warns"],
                    "num_warns": self.user_info["num_warns"],
                },
            )
            return self.user_info["warns"], self.user_info["num_warns"]

    def remove_warn(self, user_id: int):
        with INSERTION_LOCK:
            self.user_info = self.__ensure_in_db(user_id)
            self.user_info["warns"].pop()
            self.user_info["num_warns"] = len(self.user_info["warns"])
            self.update(
                {"chat_id": self.chat_id, "user_id": user_id},
                {
                    "warns": self.user_info["warns"],
                    "num_warns": self.user_info["num_warns"],
                },
            )
            return self.user_info["warns"], self.user_info["num_warns"]

    def reset_warns(self, user_id: int):
        with INSERTION_LOCK:
            self.user_info = self.__ensure_in_db(user_id)
            return self.delete_one({"chat_id": self.chat_id, "user_id": user_id})

    def get_warns(self, user_id: int):
        with INSERTION_LOCK:
            self.user_info = self.__ensure_in_db(user_id)
            return self.user_info["warns"], len(self.user_info["warns"])
     
        
    @staticmethod
    def count_all_chats_using_warns():
        with INSERTION_LOCK:
            collection = MongoDB(Warns.db_name)
            curr = collection.find_all()
            return len({i["chat_id"] for i in curr})

    @staticmethod
    def count_warned_users():
        with INSERTION_LOCK:
            collection = MongoDB(Warns.db_name)
            curr = collection.find_all()
            return len({i["user_id"] for i in curr if i["num_warns"] >= 1})

    @staticmethod
    def count_warns_total():
        with INSERTION_LOCK:
            collection = MongoDB(Warns.db_name)
            curr = collection.find_all()
            return sum(i["num_warns"] for i in curr if i["num_warns"] >= 1)


    def __ensure_in_db(self, user_id: int):
        chat_data = self.find_one({"chat_id": self.chat_id, "user_id": user_id})
        if not chat_data:
            new_data = {
                "chat_id": self.chat_id,
                "user_id": user_id,
                "warns": [],
                "num_warns": 0,
            }
            self.insert_one(new_data)
            return new_data
        return chat_data


class WarnSettings(MongoDB):
    db_name = "chat_warn_settings"

    def __init__(self, chat_id: int) -> None:
        super().__init__(self.db_name)
        self.chat_id = chat_id
        self.chat_info = self.__ensure_in_db()

    def __ensure_in_db(self):
        chat_data = self.find_one({"_id": self.chat_id})
        if not chat_data:
            new_data = {"_id": self.chat_id, "warn_mode": "none", "warn_limit": 3}
            self.insert_one(new_data)
            return new_data
        return chat_data
    def getall_warns(self, chat_id: int):
        with INSERTION_LOCK:
            self.chat_id = self.__ensure_in_db(chat_id)
            return self.chat_id["warns"], len(self.chat_id["warns"])
        
    def get_warnings_settings(self):
        with INSERTION_LOCK:
            return self.chat_info

    def set_warnmode(self, warn_mode: str = "none"):
        with INSERTION_LOCK:
            self.update({"_id": self.chat_id}, {"warn_mode": warn_mode})
            return warn_mode

    def get_warnmode(self):
        with INSERTION_LOCK:
            return self.chat_info["warn_mode"]

    def set_warnlimit(self, warn_limit: int = 3):
        with INSERTION_LOCK:
            self.update({"_id": self.chat_id}, {"warn_limit": warn_limit})
            return warn_limit

    def resetall_warns(self, chat_id: int):
        with INSERTION_LOCK:
            self.user_info = self.__ensure_in_db(chat_id)
            return self.delete_one({"chat_id": self.chat_id})

    def get_warnlimit(self):
        with INSERTION_LOCK:
            return self.chat_info["warn_limit"]

    @staticmethod
    def count_action_chats(mode: str):
        collection = MongoDB(WarnSettings.db_name)
        return collection.count({"warn_mode": mode})
