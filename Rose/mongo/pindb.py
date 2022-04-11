from threading import RLock
from Rose.mongo import MongoDB

INSERTION_LOCK = RLock()


class Pins(MongoDB):

    db_name = "antichannelpin"

    def __init__(self, chat_id: int) -> None:
        super().__init__(self.db_name)
        self.chat_id = chat_id
        self.chat_info = self.__ensure_in_db()

    def get_settings(self):
        with INSERTION_LOCK:
            return self.chat_info

    def antichannelpin_on(self):
        with INSERTION_LOCK:
            return self.set_on("antichannelpin")

    def cleanlinked_on(self):
        with INSERTION_LOCK:
            return self.set_on("cleanlinked")

    def antichannelpin_off(self):
        with INSERTION_LOCK:
            return self.set_off("antichannelpin")

    def cleanlinked_off(self):
        with INSERTION_LOCK:
            return self.set_off("cleanlinked")

    def set_on(self, atype: str):
        with INSERTION_LOCK:
            otype = "cleanlinked" if atype == "antichannelpin" else "antichannelpin"
            return self.update(
                {"_id": self.chat_id},
                {atype: True, otype: False},
            )

    def set_off(self, atype: str):
        with INSERTION_LOCK:
            otype = "cleanlinked" if atype == "antichannelpin" else "antichannelpin"
            return self.update(
                {"_id": self.chat_id},
                {atype: False, otype: False},
            )

    def __ensure_in_db(self):
        chat_data = self.find_one({"_id": self.chat_id})
        if not chat_data:
            new_data = {
                "_id": self.chat_id,
                "antichannelpin": False,
                "cleanlinked": False,
            }
            self.insert_one(new_data)
            return new_data
        return chat_data

    def migrate_chat(self, new_chat_id: int):
        old_chat_db = self.find_one({"_id": self.chat_id})
        new_data = old_chat_db.update({"_id": new_chat_id})
        self.insert_one(new_data)
        self.delete_one({"_id": self.chat_id})


       
