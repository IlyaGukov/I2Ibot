class Message:
	def __init__(self, user_id, text, subject, language, question_flag):
		self.user_id = user_id
		self.text = text
		self.subject = subject
		self.language = language
		self.question_flag = question_flag
