import queue
import threading

class UserDataBase:
    def __init__(self):
        self.data = dict()
    
    #ToDo make it async
    def add_user(self, chat_id):
        self.data[chat_id] = {'User':chat_id, 'Occupied':False, 'Language': set(), 'Themes': set()}
    
    def write_user_data(self, chat_id, data_field, user_data):
        self.data[chat_id][data_field].add(user_data)

    def change_occupation(self, chat_id):
        self.data[chat_id]['Occupied'] = not self.data[chat_id]['Occupied']
            
    def delete_user(self, chat_id):
        self.data.pop(chat_id)
    
    
class One_to_one:
    '''
    thread safe
    '''
    def __init__(self):
            self.data = dict()
            self.lock = threading.Lock()
        
    def write(self, asker_id, list_of_dodiks):
        with self.lock:
            for dod in list_of_dodiks:
                self.data[dod.get_chat_id()] = asker_id
            
    def search_and_pop(self, dodik_id):
        with self.lock:
            if dodik_id in self.data.keys():
                answer = self.data.pop(dodik_id)
            else:
                answer = False
        return answer
