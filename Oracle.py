import queue
import numpy as np
    
class Oracle:

    def __init__(self, user_db, one_to_one):
        self.question_queue = queue.Queue()
        self.release_queue = queue.Queue()
        self.user_db = user_db
        self.one_to_one = one_to_one
        
    def push_to_queue(self, question):
        self.question_queue.put(question)
        
    def find_dodiks(self, question):
        candidates = []
        for u in self.user_db.values():
            if u['Occupied'] == False and question.language == u['User'].get_language():
                candidates.append(u['User'])
        list_of_dodiks = np.random.choice(candidates, 5)
        for l in list_of_dodiks:
            self.user_db.change_occupation(l.get_chat_id())
        return list_of_dodiks
    
    def send(self,bot,list_of_dodiks,question):
        
    ### telegram API, write correspodance to SQL message DB
    
        asker_id = question.get_chat_id()
        self.one_to_one.write(asker_id, list_of_dodiks)
        
    def serve_questions(self, question):
        self.send(find_dodiks, question)
        
    def serve_question_queue(self):
        while True:
            q  = self.question_queue.get()
            ### consider exit from this loop
            if q is None:
                continue
            self.serve_questions(q)
            self.question_queue.task_done()