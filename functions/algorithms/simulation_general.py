import datetime
from classes.guest import Guest

'''
TEST FUNCTIONS
'''

def create_guests(n = None):
	# Pre-defined start_time and etas
	start_time = datetime.time(0,0,0)
	etas = [6, 3, 1, 1, 1]
	names = ['a','b','c','d','e',]
	orders = [2, 1, 1, 1, 1]

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