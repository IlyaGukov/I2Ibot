class Conversation:
    
    # ToDo: add oracle as initialization param here
    def __init__(self, question, asker_id, oracle_):
        self.oracle = oracle_
        self.question = question
        self.asker_id = asker_id
        self.answer = {}
        
    def main(self):
        self.oracle.push_to_queue(self.question)
