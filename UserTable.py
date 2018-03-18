import threading

class UserTable:
    def __init__(self):
        self.table = set()
        self.table_lock = threading.Lock()

    def user_in_table(self, chat_id_):
        with self.table_lock:
            fl = chat_id_ in self.table
        return fl

    def add_user(self, chat_id_):
        with self.table_lock:
            self.table.add(chat_id_)

    def remove_user(self, chat_id_):
        with self.table_lock:
            self.table.remove(chat_id_)