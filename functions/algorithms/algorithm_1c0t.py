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

	current_guest = future_guests[0]
	future_guests.pop(0)
	chef.q.append(current_guest)
	current_guest.wait = current_guest.arrive

	counter = 2
	print [j.name for j in chef.q]
	print [j.wait for j in chef.q]

	while counter != 0:
		counter -= 1

		if not chef.q:
			break
		
		if future_guests:
			current_guest = future_guests[0]

			# Calculate wait time for customer
			# Add to chef.q

			future_guests.pop(0)
		print [j.name for j in chef.q]
		print [j.wait for j in chef.q]
