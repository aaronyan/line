from classes import chef, guest, restaurant
import simulation_general as sg
import datetime
import numpy as np

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
			print [k.name for k in chef.q]
			print [k.wait.seconds/60 for k in chef.q]

			# Calculate wait time for customer
			# Add to chef.q

			future_guests.pop(0)
		print [j.name for j in chef.q]
		print [j.wait for j in chef.q]
