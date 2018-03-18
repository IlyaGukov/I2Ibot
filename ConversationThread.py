from Oracle import Oracle

class Conversation:
    oracle = Oracle()
    
    def __init__(self, question, asker_id):
        self.question = question
        self.asker_id = asker_id
        self.answer = {}
        
    def main(self):
        oracle.push_to_queue(self.question)
