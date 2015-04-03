import datetime

class Simulator(object):
	def __init__(self, interval = None):
		self.interval = datetime.timedelta(minutes = 1)

		if not interval:
			self.interval = datetime.timedelta(minutes = interval)