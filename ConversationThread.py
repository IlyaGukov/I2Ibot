from Oracle import Oracle

class Conversation:
	oracle = Oracle()
	
	def __init__(self, bot, question, asker_id):
		self.bot = bot
		self.question = question
		self.asker_id = asker_id
		self.answer = {}
		
	def main(self):
		oracle.push_to_queue(self.question)
		

	
	
	