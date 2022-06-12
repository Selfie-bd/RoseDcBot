from threading import RLock
from Rose.mongo import MongoDB

INSERTION_LOCK = RLock()

class db(MongoDB):
    db_name = "nightdb"
    def __init__(self) -> None:
        super().__init__(self.db_name)
  
    def disapprove(self, chat_id: int):
        with INSERTION_LOCK:
            return self.delete_one({"chat_id": chat_id})

    def approve(self, chat_id: int):
        with INSERTION_LOCK:
            fucked = self.find_one({chat_id:"chat_id"})
            if fucked:
                return 
            else:
                self.insert_one({
                "chat_id":chat_id
            })

    def all_chats(self):
        with INSERTION_LOCK:
            nightdb = self.find_all()
            chats_ids = {i["chat_id"] for i in nightdb}
            return len(chats_ids)
  