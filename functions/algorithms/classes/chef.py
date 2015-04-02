import datetime

class Chef(object):
	def __init__(self, interval = None):
		self.id = id(self)
		self.name = ''
		self.q = []
		self.wait = datetime.timedelta(minutes = 0)
		self.interval = datetime.timedelta(minutes = 5)

		if interval is not None:
			self.interval = datetime.timedelta(minutes = interval)