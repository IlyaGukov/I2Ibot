class Conversation:
    
    # ToDo: add oracle as initialization param here
    def __init__(self, question, oracle_):
        self.oracle = oracle_
        self.question = question
        self.asker_id = question.asker_id
        self.answer = {}
        
    def main(self):
        self.oracle.push_to_queue(self.question)
