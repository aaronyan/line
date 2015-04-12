import datetime
from classes.guest import Guest
import string
import numpy as np

'''
TEST FUNCTIONS
'''

def create_guests(mode = None, n = None):

	if n != None:
		d = dict.fromkeys(string.ascii_lowercase, 0)
		etas = [np.random.randint(1,6) for i in range(n)]
		names = [i for i in d]
		orders = [np.random.randint(1,6) for i in range(n)]

	# Pre-defined etas
	if mode == 'case_1':
		etas = [6, 3, 1, 1, 1]
		names = ['a','b','c','d','e',]
		orders = [2, 1, 1, 1, 1]
		n = 5

	arrivals = []
	for i in range(n):
		new_guest = Guest()
		# new_guest.eta = np.random.random_integers(1,3)*5
		new_guest.arrive = datetime.timedelta(minutes=etas[i])
		new_guest.name = names[i]
		new_guest.id = 'gst'+str(i)
		new_guest.orders = orders[i]
		new_guest.prep = orders[i]*1
		arrivals.append(new_guest)
	return arrivals
