import queue
import threading

class UserDataBase:
	def __init__(self):					
		self.data = {}
		
	def write_user(self, user):
		self.data[user.get_chat_id()] = {'User':user,'Occupied':False}
		
	def change_occupation(self,chat_id):
		self.data[chat_id]['Occupied'] = not self.data[chat_id]['Occupied']
			
	def delete_user(self,chat_id)
		self.data.pop(chat_id)
	
	
class One_to_one:
	#thread safe

	def __init__(self, lock):					
			self.data = {}
		
	def write(self, asker_id, list_of_dodiks):
		with lock:
			for dod in list_of_dodiks:
				self.data[dod.get_chat_id()] = asker_id
			
	def search_and_pop(self,dodik_id):
		lock.acquire()
		try:
			if dodik_id in self.data.keys():
				answer = self.data.pop(dodik_id)
				lock.release()
				return answer
			else:
				return False
		finally:
			lock.release()
			
	
	
	
	