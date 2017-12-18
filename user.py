
class User:

	def __init__(self, nationality, language, chat_id):
		self.nationality = nationality
		self.language = language
		self.score = 0
		self.chat_id = chat_id
	
	def reward(self,rew):
		self.score += rew
	
	def get_language(self):
		return self.language
	
	def get_nationality(self):
		return self.nationality

	def get_score(self):
		return self.score
		
	def get_chat_id(self):
		return self.chat_id
		
		