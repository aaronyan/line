from classes import chef, guest, restaurant
import simulation_general as sg
import datetime
import numpy as np

def calc_guest_wait(current_guest, restaurant):
	for j,chef in enumerate(restaurant.chefs):
		# If the chef's queue is empty, the current guest wait time = arrive
		if chef.q == []:
			restaurant.chefs[0].q.append(current_guest)
			return current_guest.arrive

		q_inspect = [i for i in chef.q]

		for i, guest in enumerate(chef.q):
			front_wait = chef.q[i].wait
			print "iteration =", i, "and front_wait =", front_wait

			if i == 0:
				if current_guest.arrive + chef.prep_time < front_wait or \
				   (current_guest.arrive == datetime.timedelta(minutes = 1) and \
				   	current_guest.arrive < front_wait):
					print "guest found an opening in the front!"
					restaurant.chefs[j].q.insert(i, current_guest)
					current_guest.wait = current_guest.arrive
					return current_guest.wait
				elif len(chef.q) != 1:
					back_wait = chef.q[i+1].wait
					if front_wait + chef.prep_time < back_wait:
						print "guest found an opening in the second to last!"
						restaurant.chefs[j].q.insert(i+1, current_guest)
						current_guest.wait = front_wait + chef.prep_time
						return current_guest.wait
			elif i > 0 and i < (len(chef.q)-1):
				print "back_wait =", back_wait
				back_wait = chef.q[i+1].wait
				if front_wait + chef.prep_time < back_wait:
					print "guest found an opening!"
					restaurant.chefs[j].q.insert(i+1, current_guest)
					current_guest.wait = front_wait + chef.prep_time
					return current_guest.wait
				elif current_guest.arrive + chef.prep_time < front_wait:
					print "guest found an opening in the second to last!"
					print current_guest.arrive + chef.prep_time, front_wait
					restaurant.chefs[j].q.insert(i, current_guest)
					current_guest.wait = current_guest.arrive + chef.prep_time
					return current_guest.wait
				else:
					continue
			else:
				print "guest found an opening in the back!"
				restaurant.chefs[j].q.insert(i+1, current_guest)
				current_guest.wait = front_wait + chef.prep_time
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
			print "wait time for", restaurant.chefs[i].q[j].name, "=", restaurant.chefs[i].q[j].wait
			if restaurant.chefs[i].q[j].wait == datetime.timedelta(minutes = 0):
				restaurant.chefs[i].q[j].served =  True
				index_remove.append(j)
		for k in sorted(index_remove, key=int, reverse=True):
			restaurant.chefs[i].q.pop(k)
	print "index_remove =", index_remove

if __name__ == "__main__":
	# Create restaurant, chef, and customer objects
	restaurant = restaurant.Restaurant()
	chef = chef.Chef(idn = "aaron")
	restaurant.chefs.append(chef)

	future_guests = sg.create_guests(n=5)
	restaurant.confirmed_guests = [g for g in future_guests]

	# Add the first guest to the chef queue
	current_guest = future_guests[0]
	future_guests.pop(0)
	chef.q.append(current_guest)
	current_guest.wait = current_guest.arrive
	print "\nNEW GUEST"
	print current_guest.name, current_guest.arrive, current_guest.wait
	print [k.name for k in chef.q]
	print [k.wait.seconds/60 for k in chef.q]

	counter = 2
	increment_interval(restaurant)
	clean_up_chef_q(restaurant)

	# Serve all the guests
	while counter != 0:
		counter -= 1

		if not chef.q:
			print "\nchef.q is empty"
			break
		
		if future_guests:
			current_guest = future_guests[0]

			print "\nNEW GUEST"
			print current_guest.name, current_guest.arrive, current_guest.wait
			current_guest_wait = calc_guest_wait(current_guest, restaurant)
			# print "calculated wait time =", current_guest_wait
			print [k.name for k in chef.q]
			print [k.wait.seconds/60 for k in chef.q]

			increment_interval(restaurant)
			clean_up_chef_q(restaurant)
			future_guests.pop(0)

		print [j.name for j in chef.q]
		print [j.wait for j in chef.q]
