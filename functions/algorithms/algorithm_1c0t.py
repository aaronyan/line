from classes import chef, guest, restaurant
import simulation_general as sg
import datetime
import numpy as np

# Caclulate guest wait time
def calc_guest_wait(current_guest, restaurant):
	for j,chef in enumerate(restaurant.chefs):
		# If the chef's queue is empty, the current guest wait time = arrive
		if chef.q == []:
			restaurant.chefs[0].q.append(current_guest)
			if current_guest.arrive > current_guest.orders*chef.prep_time:
				return current_guest.arrive
			else:
				return current_guest.orders*chef.prep_time

		q_inspect = [i for i in chef.q]

		# Check openings in chef queue
		for i, guest in enumerate(chef.q):
			front_wait = guest.wait
			front_min = front_wait - guest.orders*chef.prep_time
			current_arrive = current_guest.arrive
			current_prep = current_guest.orders*chef.prep_time
			print "checking guest",guest.name

			# If the queue is only one person long or looking at the first person in the queue
			if i == 0:
				if current_prep <= front_min and current_arrive <= front_min:
					print "guest found an opening in the front!"
					restaurant.chefs[j].q.insert(i, current_guest)
					current_guest.wait = current_guest.arrive
					return current_guest.wait
					# If the queue is two people long
				elif len(chef.q) != 1:
					back_wait = chef.q[i+1].wait
					back_min = back_wait - chef.q[i+1].orders*chef.prep_time
					if current_prep <= back_min and front_wait + current_prep <= back_min and current_arrive <= back_min:
						print "guest found an opening second in line!"
						restaurant.chefs[j].q.insert(i+1, current_guest)
						current_guest.wait = front_wait + current_prep
						return current_guest.wait
				else:
					print "guest found an opening in the back!"
					restaurant.chefs[j].q.insert(i+1, current_guest)
					if current_arrive <= front_wait:
						current_guest.wait = front_wait + current_prep
					else:
						current_guest.wait = current_arrive
					return current_guest.wait
			# If the queue is anyone not the first or last person in the queue
			elif i > 0 and i < (len(chef.q)-1):
				back_wait = chef.q[i+1].wait
				back_min = back_wait - chef.q[i+1].orders*chef.prep_time
				if current_prep <= back_min and front_wait + current_prep <= back_min and current_arrive <= back_min:
						print "guest found an opening second in line with queue > 2!"
						restaurant.chefs[j].q.insert(i+1, current_guest)
						current_guest.wait = front_wait + current_prep
						return current_guest.wait
			# If the person is the last person in the queue and/or cannot find an opening in the queue
			else:
				print "guest found an opening in the back!"
				restaurant.chefs[j].q.insert(i+1, current_guest)
				if current_arrive <= front_wait:
					current_guest.wait = front_wait + current_prep
				else:
					current_guest.wait = current_arrive
				return current_guest.wait


def increment_interval(restaurant):
	for i, chef in enumerate(restaurant.chefs):
		for j, guest in enumerate(chef.q):
			if not restaurant.chefs[i].q[j].served:
				restaurant.chefs[i].q[j].wait -= restaurant.chefs[i].prep_time
				restaurant.chefs[i].q[j].arrive -= restaurant.chefs[i].prep_time

def clean_up_chef_q(restaurant):
	index_remove = []
	for i, chef in enumerate(restaurant.chefs):
		for j, guest in enumerate(chef.q):
			# print "wait time for", restaurant.chefs[i].q[j].name, "=", restaurant.chefs[i].q[j].wait
			if restaurant.chefs[i].q[j].wait == datetime.timedelta(minutes = 0):
				restaurant.chefs[i].q[j].served =  True
				index_remove.append(j)
		for k in sorted(index_remove, key=int, reverse=True):
			restaurant.chefs[i].q.pop(k)
	# print "index_remove =", index_remove

def no_algorithm_time(future_guests, restaurant):
	
	# add minutes to wait time to normalize based on index
	for i, guest in enumerate(future_guests):
		guest.arrive = guest.arrive + datetime.timedelta(minutes=i)

	# order the future guests by arrival 
	future_guests = sg.mergesort(future_guests)

	# simulate the no algorithm queuing
	look_at_guests = [g for g in future_guests]
	front = look_at_guests[0]
	front.wait = front.arrive + front.orders * restaurant.prep_time
	look_at_guests.pop(0)
	# print len(look_at_guests)

	while look_at_guests:
		focus = look_at_guests.pop(0)
		focus_min = focus.arrive + focus.orders * restaurant.prep_time

		if focus_min <= front.wait:
			focus.wait = front.wait + focus.orders * restaurant.prep_time
		elif focus_min > front.wait:
			focus.wait = focus_min

	return future_guests[-1].wait.seconds/60

def algorithm_time(future_guests, restaurant):
	# Add the first guest to the chef queue
	counter = 0
	current_guest = future_guests[0]
	future_guests.pop(0)
	chef.q.append(current_guest)
	current_guest.wait = current_guest.arrive
	print "\ncounter = ", counter
	print "NEW GUEST"
	print "guests: ", [k.name for k in chef.q]
	print "wait: ", [k.wait.seconds/60 for k in chef.q]
	print "prep: ", [k.prep.seconds/60 for k in chef.q]

	# Serve all the guests
	while chef.q:
		counter += 1

		increment_interval(restaurant)
		clean_up_chef_q(restaurant)

		if future_guests:
			current_guest = future_guests[0]

			print "\ncounter = ", counter
			print "NEW GUEST"
			print current_guest.name, current_guest.arrive, current_guest.wait
			current_guest.wait = calc_guest_wait(current_guest, restaurant)
			print "calculated wait time =", current_guest.wait
			print "guests: ", [k.name for k in chef.q]
			print "wait: ", [k.wait.seconds/60 for k in chef.q]
			print "prep: ", [k.prep.seconds/60 for k in chef.q]
			clean_up_chef_q(restaurant)
			future_guests.pop(0)
		else:
			print "\ncounter = ", counter
			print "NO MORE"
			print "guests: ", [k.name for k in chef.q]
			print "wait: ", [k.wait.seconds/60 for k in chef.q]
			print "prep: ", [k.prep.seconds/60 for k in chef.q]
			clean_up_chef_q(restaurant)

	# print "\ncounter = ", counter
	return counter

if __name__ == "__main__":
	# Create restaurant, chef, and customer objects
	restaurant = restaurant.Restaurant()
	chef = chef.Chef(idn = "aaron")
	restaurant.chefs.append(chef)
	copy_guests = []

	# future_guests = sg.create_guests(mode = 'case_1')
	# future_guests = sg.create_guests(mode = 'case_2')
	# future_guests = sg.create_guests(mode = 'case_3')
	# future_guests = sg.create_guests(mode = 'case_4')
	future_guests = sg.create_guests(n=5)
	sg.copy_guests(future_guests, copy_guests)

	print "guests: ", [g.name for g in future_guests]
	print "arrive: ", [g.arrive.seconds/60 for g in future_guests]

	# Compare with the algorithm
	alg_count = algorithm_time(future_guests, restaurant)
	
	# Compare with the no_algorithm
	no_alg_count = no_algorithm_time(copy_guests, restaurant)

	print alg_count
	print no_alg_count


