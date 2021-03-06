import queue
import threading
import pickle

class UserDataBase:
    def __init__(self):
        try:
            with open('user_db', 'rb') as f:
                self.data = pickle.load(f)
        except (FileNotFoundError, EOFError, IOError) as e:
            self.data = dict()

    
    #ToDo make it async
    def add_user(self, chat_id, user_name):
        self.data[chat_id] = {'Name':user_name, 'Occupied':False, 'Languages': set(), 'Themes': set()}
        with open('user_db', 'wb') as f:
            pickle.dump(self.data, f, pickle.HIGHEST_PROTOCOL)

    def get_user(self, chat_id):
        return self.data[chat_id]

    def get_all_user_ids(self):
        return self.data.keys()

    def write_user_data(self, chat_id, data_field, user_data):
        self.data[chat_id][data_field].add(user_data)
        with open('user_db', 'wb') as f:
            pickle.dump(self.data, f, pickle.HIGHEST_PROTOCOL)

    def change_occupation(self, chat_id):
        self.data[chat_id]['Occupied'] = not self.data[chat_id]['Occupied']
            
    def delete_user(self, chat_id):
        self.data.pop(chat_id)
        with open('user_db', 'wb') as f:
            pickle.dump(self.data, f, pickle.HIGHEST_PROTOCOL)
    
    
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
                self.data[dod] = asker_id
            
    def search_and_pop(self, dodik_id):
        with self.lock:
            if dodik_id in self.data.keys():
                answer = self.data.pop(dodik_id)
            else:
                answer = False
        return answer
