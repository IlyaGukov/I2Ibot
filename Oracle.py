from telegram.ext.dispatcher import run_async
import queue
import numpy as np

class Oracle:

    def __init__(self, bot_, user_db, one_to_one):
        self.question_queue = queue.Queue()
        self.release_queue = queue.Queue()
        self.bot = bot_
        self.user_db = user_db
        self.one_to_one = one_to_one
        self.serve_question_queue()
        
    def push_to_queue(self, question):
        self.question_queue.put(question)
        
    def find_dodiks(self, question):
        candidates = []
        # data is private field, should be done in another way
        for user_id in self.user_db.get_all_user_ids():
            user_data = self.user_db.get_user(user_id)
            if ((user_data['Occupied'] == False) and
                (question.language in user_data['Languages'])):
                candidates.append(user_id)
        number_of_dodiks = 5 if len(candidates) >= 5 else len(candidates)
        list_of_dodiks = np.random.choice(candidates, number_of_dodiks)
        for dodik_id in list_of_dodiks:
            self.user_db.change_occupation(dodik_id)
        return list_of_dodiks
    
    @run_async
    def send(self, dodik, question):
    ### telegram API, write correspodance to SQL message DB
        print(dodik, question.text)
        self.bot.send_message(chat_id = dodik, text = question.text)
        
    def serve_questions(self, question):
        list_of_dodiks = self.find_dodiks(question)
        for dodik in list_of_dodiks:
            # cast to int is needed as random.choice make Ids int64 what is bad for telegram API    
            self.send(int(dodik), question)
        self.one_to_one.write(question.asker_id, list_of_dodiks)

    @run_async
    def serve_question_queue(self):
        while True:
            q  = self.question_queue.get()
            ### consider exit from this loop
            if q is None:
                continue
            self.serve_questions(q)
            # don't sure if task_done needed?
            # self.question_queue.task_done()