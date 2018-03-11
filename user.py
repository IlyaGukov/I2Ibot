
class User:

	def __init__(self, language, chat_id):
		self.language = language
		self.score = 0
		self.chat_id = chat_id
	
	def get_language(self):
		return self.language	

	def get_score(self):
		return self.score
		
	def get_chat_id(self):
		return self.chat_id
		
		