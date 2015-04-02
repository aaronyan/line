import datetime

class Guest(object):
	def __init__(self):
		self.id = id(self)
		self.name = ''
		self.location = ''
		self.distance = 0
		self.arrive = datetime.timedelta(minutes = 0)
		self.wait = datetime.timedelta(minutes = 0)
		self.request = datetime.datetime(2015,1,1,0,0,0)
		self.q_num = 0