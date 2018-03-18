from Oracle import Oracle

class Conversation:
    
    # ToDo: add oracle as initialization param here
    def __init__(self, question, asker_id):
        self.question = question
        self.asker_id = asker_id
        self.answer = {}
        
    def main(self):
        oracle.push_to_queue(self.question)
