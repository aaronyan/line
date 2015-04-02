import datetime

class Table(object):
	def __init__(self):
		self.idn = ''
		self.q = []
		self.min_wait = datetime.timedelta(minutes = 0)