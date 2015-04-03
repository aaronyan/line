from classes import chef, guest, restaurant
import test_functions as tf
import datetime
import numpy as np

if __name__ == "__main__":
	# Create restaurant, chef, and customer objects
	restaurant = restaurant.Restaurant()
	chef = chef.Chef(idn = "aaron")
	restaurant.chefs.append(chef)

	future_guests = tf.create_guests(n=5)
	restaurant.confirmed_guests = [g for g in future_guests]