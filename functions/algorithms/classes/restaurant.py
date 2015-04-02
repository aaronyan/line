import datetime

class Restaurant(object):
	def __init__(self):
		self.idn = ''
		self.location = ''
		self.q = []
		self.min_wait = datetime.timedelta(minutes = 0)
		self.guest_list = None
		self.interval = datetime.timedelta(minutes = 5)