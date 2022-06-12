from threading import RLock
from Rose.mongo import MongoDB

INSERTION_LOCK = RLock()

class fsubdatabase(MongoDB):
    db_name = "fsubdata"
    def __init__(self) -> None:
        super().__init__(self.db_name)
  
    def current(self,chat_id:int):
        with INSERTION_LOCK:
            fucked = self.find_one({chat_id:"channel"})
            if not fucked:
                return 
            
    def disapprove(self, chat_id: int):
        with INSERTION_LOCK:
            return self.delete_one({"chat_id": chat_id})
    
    def addchannel(self,chat_id : int, channel : int):
        with INSERTION_LOCK:
            self.insert_one({
                "chat_id":chat_id,
                "channel":channel
            })

   