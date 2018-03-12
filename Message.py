class Message:
	def __init__(self, chat_id, text, subject, language):
		self.chat_id = chat_id
		self.text = text
		self.subject = subject
		self.language = language
	
	def get_chat_id(self):
		return self.chat_id
		
	

