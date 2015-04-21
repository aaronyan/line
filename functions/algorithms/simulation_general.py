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
		etas = [np.random.randint(1,4) for i in range(n)]
		names = [i for i in d]
		orders = [np.random.randint(1,4) for i in range(n)]

	# Pre-defined etas
	if mode == 'case_1':
		etas = [6, 3, 1, 5, 1]
		names = ['a','b','c','d','e',]
		orders = [2, 1, 1, 1, 1]
		n = 5

	if mode == 'case_2':
		etas = [1, 3, 3, 2]
		names = ['a','b','c','d']
		orders = [2, 1, 1, 1]
		n = 4

	if mode == 'case_3':
		etas = [3, 2, 3, 3, 1]
		names = ['a','b','c','d','e']
		orders = [1, 1, 1, 1, 1]
		n = 5

	if mode == 'case_4':
		etas = [2, 2, 1, 1, 3]
		names = ['a','b','c','d','e']
		orders = [1, 1, 1, 1, 1]
		n = 5

	arrivals = []
	for i in range(n):
		new_guest = Guest()
		# new_guest.eta = np.random.random_integers(1,3)*5
		new_guest.arrive = datetime.timedelta(minutes=etas[i])
		new_guest.name = names[i]
		new_guest.id = 'gst'+str(i)
		new_guest.orders = orders[i]
		new_guest.prep = datetime.timedelta(minutes=orders[i]*1)
		arrivals.append(new_guest)
	return arrivals

def copy_guests(A, B):
	for i in A:
		new_guest = Guest()
		new_guest.arrive = i.arrive
		new_guest.name = i.name
		new_guest.id = i.id
		new_guest.orders = i.orders
		new_guest.prep = i.prep
		B.append(new_guest)

def merge(a, b):
	if len(a)*len(b) == 0:
		return a + b

	v = (a[0].arrive < b[0].arrive and a or b).pop(0)
	return [v] + merge(a, b)

def mergesort(future_guests):
	if len(future_guests) <= 1:
		return future_guests

	m = len(future_guests)/2
	return merge(mergesort(future_guests[:m]), mergesort(future_guests[m:]))