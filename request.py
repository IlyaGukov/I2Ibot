import random
class Request:
	
	def __init__(self,bot, asker, question,):
		self.churka = asker.get_chat_id
      	self.question = question
		self.bot = bot
		self.answers = {}
	
	def ask_dodiks(self,number_of_dodiks,dodik_array):
		list_of_dodiks = random.sample(dodik_array,number_of_dodiks)
		for dod in ask_dodiks:
			self.bot.send_message(chat_id=dod.get_chat_id, text = question)
		return list_of_dodiks
	
	def add_answer(self,user,text):
		self.answers[user] = text
		
	def send_answers(self):
		for k in self.answers.keys():
			self.bot.send_message(chat_id = self.churka, text = answers[k])