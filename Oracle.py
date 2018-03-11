import queue
class Sender:

	def send(bot,list_of_dodiks):
	### telegram API, write correspodance to SQL message DB
		
	
class Oracle:

	def __init__(self):
		self.question_queue = queue.Queue()
		self.release_queue = queue.Queue()
	
	def push_to_query(self,question):
		self.question_queue.put(question)
		
	def find_dodiks(self,question):
	### SQLmagic
		return list_of_dodiks
	
	def serve_questions(self,question):
		### SQLmagic mark users as asked
		Sender.send(find_dodiks)
		
	def serve_question_queue(self):
		while True:
			q  = question_queue.get()
			### consider exit from this loop
			if q is None:
				continue
			self.serve_questions(q)
			question_queue.task_done()
		
			
			
		