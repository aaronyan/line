import datetime

class Chef(object):
	def __init__(self, idn = None, prep_time = None):
		self.idn = ''
		self.name = ''
		self.q = []
		self.prep_time = datetime.timedelta(minutes = 1)

		if idn is not None:
			self.idn = idn

		if prep_time is not None:
			self.prep_time = datetime.timedelta(minutes = prep_time)