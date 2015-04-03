import datetime

class Restaurant(object):
	def __init__(self):
		self.chefs = []
		self.confirmed_guests = []
		self.prep_time = datetime.timedelta(minutes = 1)