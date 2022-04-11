from threading import RLock
from Rose.mongo import MongoDB
from Rose.utils.msg_types import Types

INSERTION_LOCK = RLock()


class Filters(MongoDB):
    db_name = "chat_filters"

    def __init__(self) -> None:
        super().__init__(self.db_name)

    def save_filter(
        self,
        st: int,
        keyword: str,
        filter_reply: str,
        msgtype: int = Types.TEXT,
        fileid="",
    ):
        with INSERTION_LOCK:
            curr = self.find_one({"chat_id": st, "keyword": keyword})
            if curr:
                return False
            return self.insert_one(
                {
                    "chat_id": st,
                    "keyword": keyword,
                    "filter_reply": filter_reply,
                    "msgtype": msgtype,
                    "fileid": fileid,
                },
            )


    def get_filter(self, st: int, keyword: str):
        with INSERTION_LOCK:
            curr = self.find_one({"chat_id": st, "keyword": keyword})
            if curr:
                return curr
            return "Filter does not exist!"

    def get_all_filters(self, st: int):
        with INSERTION_LOCK:
            curr = self.find_all({"chat_id": st})
            if curr:
                filter_list = {i["keyword"] for i in curr}
                return list(filter_list)
            return []

    def rm_filter(self, st: int, keyword: str):
        with INSERTION_LOCK:
            curr = self.find_one({"chat_id": st, "keyword": keyword})
            if curr:
                self.delete_one(curr)
                return True
            return False

    def rm_all_filters(self, chat_id: int):
        with INSERTION_LOCK:
            return self.delete_one({"chat_id": chat_id})

    def count_filters_all(self):
        with INSERTION_LOCK:
            return self.count()


    def count_filter_aliases(self):
        with INSERTION_LOCK:
            curr = self.find_all()
            if curr:
                return len(
                    [z for z in (i["keyword"].split("|") for i in curr) if len(z) >= 2],
                )
            return 0

    def count_filters_chats(self):
        with INSERTION_LOCK:
            filters = self.find_all()
            chats_ids = {i["chat_id"] for i in filters}
            return len(chats_ids)

    def count_all_filters(self):
        with INSERTION_LOCK:
            return self.count()

    def count_filter_type(self, ntype):
        with INSERTION_LOCK:
            return self.count({"msgtype": ntype})

    def load_from_db(self):
        with INSERTION_LOCK:
            return self.find_all()

    def migrate_chat(self, old_chat_id: int, new_chat_id: int):
        with INSERTION_LOCK:
            old_chat_db = self.find_one({"_id": old_chat_id})
            if old_chat_db:
                new_data = old_chat_db.update({"_id": new_chat_id})
                self.delete_one({"_id": old_chat_id})
                self.insert_one(new_data)