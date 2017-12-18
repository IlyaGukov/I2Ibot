
class User:

	def __init__(self, nationality, language, chat_id):
		self.nationality = nationality
      		self.language = language
		self.score = 0
	
   
	def reward(self,rew):
     		self.score += rew
