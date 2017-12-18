import random
class Request:
	
	def __init__(self,bot, asker, question,):
		self.churka = asker.get_chat_id
      	self.question = question
		self.bot = bot
		self.answers = {}
	
	def ask_dodiks(number_of_dodiks,dodik_array):
		list_of_dodiks = random.sample(dodik_array,number_of_dodiks)
		for dod in ask_dodiks:
			bot.send_message(chat_id=dod.get_chat_id, text = question)
	
	def add_answer(user,text):
		answers[user] = text
		
	def send_answers():
		for k in self.answers.keys():
			bot.send_message(chat_id = self.churka, text = answers[k])