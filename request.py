import random
class Request:
	
	def __init__(self,bot, asker, question):
		self.churka = asker
		self.question = question
		self.bot = bot
		self.answers = {}
		self.number_of_answers = 0
	
	def ask_dodiks(self,number_of_dodiks,dodik_array):
		list_of_dodiks = random.sample(dodik_array,number_of_dodiks)
		for dod in list_of_dodiks:
			self.bot.send_message(chat_id=dod.get_chat_id(), text = self.question)
		return list_of_dodiks
	
	def number_of_answers(self):
		return self.number_of_answers

	def add_answer(self,user,text):
		self.number_of_answers += 1
		self.answers[user] = text
		
	def send_answers(self):
		for k in self.answers.keys():
			self.bot.send_message(chat_id = self.churka, text = self.answers[k])