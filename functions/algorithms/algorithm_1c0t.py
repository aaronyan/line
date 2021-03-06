from classes import chef, guest, restaurant
import simulation_general as sg
import datetime
import numpy as np
import pandas as pd

# Caclulate guest t2s time
def calc_guest_t2s(current_guest, restaurant):
	for j,chef in enumerate(restaurant.chefs):
		# If the chef's queue is empty, the current guest t2s time = arrive
		if chef.q == []:
			restaurant.chefs[0].q.append(current_guest)
			if current_guest.arrive > current_guest.orders*chef.prep_time:
				return current_guest.arrive
			else:
				return current_guest.orders*chef.prep_time

		q_inspect = [i for i in chef.q]

		# Check openings in chef queue
		for i, guest in enumerate(chef.q):
			front_t2s = guest.t2s
			current_arrive = current_guest.arrive
			current_prep = current_guest.orders*chef.prep_time

			# If the queue is only one person long or looking at the first person in the queue
			if i == 0:
				if current_prep < front_t2s and current_arrive < front_t2s:
					# print "guest found an opening in the front!"
					restaurant.chefs[j].q.insert(i, current_guest)
					current_guest.t2s = current_guest.arrive
					current_guest.wait = current_guest.t2s - current_guest.arrive
					return current_guest.t2s
					# If the queue is two people long
				elif len(chef.q) != 1:
					back_t2s = chef.q[i+1].t2s
					back_min = back_t2s - chef.q[i+1].orders*chef.prep_time
					if current_prep <= back_min and front_t2s + current_prep <= back_min and current_arrive <= back_min:
						# print "guest found an opening second in line!"
						restaurant.chefs[j].q.insert(i+1, current_guest)
						current_guest.t2s = front_t2s + current_prep
						current_guest.wait = current_guest.t2s - current_guest.arrive
						return current_guest.t2s
				else:
					# print "guest found an opening in the back!"
					restaurant.chefs[j].q.insert(i+1, current_guest)
					if current_arrive <= front_t2s:
						current_guest.t2s = front_t2s + current_prep
					else:
						current_guest.t2s = current_arrive
					current_guest.wait = current_guest.t2s - current_guest.arrive
					return current_guest.t2s
			# If the queue is anyone not the first or last person in the queue
			elif i > 0 and i < (len(chef.q)-1):
				back_t2s = chef.q[i+1].t2s
				back_min = back_t2s - chef.q[i+1].orders*chef.prep_time
				if current_prep <= back_min and front_t2s + current_prep <= back_min and current_arrive <= back_min:
						# print "guest found an opening second in line with queue > 2!"
						restaurant.chefs[j].q.insert(i+1, current_guest)
						current_guest.t2s = front_t2s + current_prep
						current_guest.wait = current_guest.t2s - current_guest.arrive
						return current_guest.t2s
			# If the person is the last person in the queue and/or cannot find an opening in the queue
			else:
				# print "guest found an opening in the back!"
				restaurant.chefs[j].q.insert(i+1, current_guest)
				if current_arrive <= front_t2s:
					current_guest.t2s = front_t2s + current_prep
				else:
					current_guest.t2s = current_arrive
				current_guest.wait = current_guest.t2s - current_guest.arrive
				return current_guest.t2s


def increment_interval(restaurant):
	for i, chef in enumerate(restaurant.chefs):
		for j, guest in enumerate(chef.q):
			if not restaurant.chefs[i].q[j].served:
				restaurant.chefs[i].q[j].t2s -= restaurant.chefs[i].prep_time
				restaurant.chefs[i].q[j].arrive -= restaurant.chefs[i].prep_time

def clean_up_chef_q(restaurant):
	index_remove = []
	for i, chef in enumerate(restaurant.chefs):
		for j, guest in enumerate(chef.q):
			# print "t2s time for", restaurant.chefs[i].q[j].name, "=", restaurant.chefs[i].q[j].t2s
			if restaurant.chefs[i].q[j].t2s == datetime.timedelta(minutes = 0):
				restaurant.chefs[i].q[j].served =  True
				index_remove.append(j)
		for k in sorted(index_remove, key=int, reverse=True):
			restaurant.chefs[i].q.pop(k)
	# print "index_remove =", index_remove

def no_algorithm_time(future_guests, restaurant):
	
	out = {}
	copy_of_guests = [g for g in future_guests]

	# add minutes to t2s time to normalize based on index
	for i, guest in enumerate(future_guests):
		guest.arrive = guest.arrive + datetime.timedelta(minutes=i)

	# order the future guests by arrival 
	future_guests = sg.mergesort(future_guests)

	# simulate the no algorithm queuing
	look_at_guests = [g for g in future_guests]
	front = look_at_guests.pop(0)
	front.t2s = front.arrive + front.orders * restaurant.prep_time
	front.wait = front.t2s - front.arrive

	while look_at_guests:
		focus = look_at_guests.pop(0)
		focus.prep = focus.orders * restaurant.prep_time

		if focus.arrive > front.t2s:
			focus.t2s = focus.arrive + focus.prep
		else:
			focus.t2s = front.t2s + focus.prep

		focus.wait = focus.t2s - focus.arrive
		front = focus

	# Sum up the waited time for each customer
	wait_sum = datetime.timedelta(minutes=0)
	for g in copy_of_guests:
		wait_sum += g.wait
	wait_avg_tv = float(wait_sum.seconds)/len(copy_of_guests)
	wait_avg = float(wait_avg_tv)/60

	out['rest_time_finish'] = future_guests[-1].t2s.seconds/60
	out['guest_wait_avg'] = wait_avg

	print "names:   ", [g.name for g in future_guests]
	print "arrives: ", [g.arrive.seconds/60 for g in future_guests]
	print "orders:  ", [g.orders for g in future_guests]
	print "t2s:     ", [g.t2s.seconds/60 for g in future_guests]
	print "wait:    ", [g.wait.seconds/60 for g in future_guests]

	return out

def algorithm_time(future_guests, restaurant):
	# Add the first guest to the chef queue
	out = {}
	rest_counter = 0
	copy_of_guests = [g for g in future_guests]
	current_guest = future_guests.pop(0)
	chf = restaurant.chefs[0]
	chf.q.append(current_guest)

	if current_guest.arrive > current_guest.orders * restaurant.prep_time:
		current_guest.t2s = current_guest.arrive
	else:
		current_guest.t2s = current_guest.orders * restaurant.prep_time
	print "\ncounter = ", rest_counter
	print "NEW GUEST"
	print "guests: ", [k.name for k in chf.q]
	print "t2s: ", [k.t2s.seconds/60 for k in chf.q]
	print "prep: ", [k.prep.seconds/60 for k in chf.q]

	# Serve all the guests
	while chf.q:
		rest_counter += 1

		increment_interval(restaurant)
		clean_up_chef_q(restaurant)

		if future_guests:
			current_guest = future_guests[0]

			print "\ncounter = ", rest_counter
			print "NEW GUEST"
			print current_guest.name, current_guest.arrive, current_guest.orders
			current_guest.t2s = calc_guest_t2s(current_guest, restaurant)
			print "calculated t2s time =", current_guest.t2s
			print "guests: ", [k.name for k in chf.q]
			print "t2s: ", [k.t2s.seconds/60 for k in chf.q]
			print "prep: ", [k.prep.seconds/60 for k in chf.q]
			clean_up_chef_q(restaurant)
			future_guests.pop(0)
		else:
			print "\ncounter = ", rest_counter
			print "NO MORE"
			print "guests: ", [k.name for k in chf.q]
			print "t2s: ", [k.t2s.seconds/60 for k in chf.q]
			print "prep: ", [k.prep.seconds/60 for k in chf.q]
			clean_up_chef_q(restaurant)


	# Sum up the waited time for each customer
	wait_sum = datetime.timedelta(minutes=0)
	for g in copy_of_guests:
		wait_sum += g.wait
	wait_avg = float(wait_sum.seconds)/len(copy_of_guests)
	wait_avg = float(wait_avg)/60

	print
	print "names:   ", [g.name for g in copy_of_guests]
	# print "arrives: ", [g.arrive.seconds/60 for g in copy_of_guests]
	print "orders:  ", [g.orders for g in copy_of_guests]
	# print "t2s:     ", [g.t2s.seconds/60 for g in copy_of_guests]
	print "wait:    ", [g.wait.seconds/60 for g in copy_of_guests], "\n"

	out['rest_time_finish'] = rest_counter
	out['guest_wait_avg'] = wait_avg

	# print "\ncounter = ", rest_counter
	return out

def simulate_basic_max_cust_size(sim_num, sample_num, file_name):
	data = pd.DataFrame()

	for i in range(sim_num):
		print i
		diff = 0
		diff2 = 0
		for j in range(sample_num):
			sample_n = i + 3
			rest = restaurant.Restaurant()
			chf = chef.Chef(idn = "aaron")
			rest.chefs.append(chf)
			copy_guests = []
			copycopy_guests = []

			# future_guests = sg.create_guests(mode = 'case_6')
			future_guests = sg.create_guests(n=sample_n, p_eta=4, p_order=4)
			sg.copy_guests(future_guests, copy_guests)
			sg.copy_guests(future_guests, copycopy_guests)
			# print "future guests: ", [k.name for k in future_guests]
			# print "future guests arrives: ", [k.arrive.seconds/60 for k in future_guests]

			# Compare with the algorithm
			alg_out = algorithm_time(future_guests, rest)

			# Compare with the no_algorithm
			no_alg_out = no_algorithm_time(copy_guests, rest)

			alg_col = 'alg_rest'+str(i)
			no_alg_col ='no_alg_rest'+str(i)
			rest_diff_col = 'rest_diff'+str(i)
			rest_percent_col = 'rest_diff_percent'+str(i)

			alg_guest_avg_col = 'alg_guest_wait_avg'+str(i)
			no_alg_guest_avg_col = 'no_alg_guest_wait_avg'+str(i)
			guest_diff_col = 'guest_diff'+str(i)
			guest_percent_col = 'guest_diff_percent'+str(i)

			data.loc[j,alg_col] = alg_out['rest_time_finish']
			data.loc[j,no_alg_col] = no_alg_out['rest_time_finish']

			data.loc[j,alg_guest_avg_col] = alg_out['guest_wait_avg']
			data.loc[j,no_alg_guest_avg_col] = no_alg_out['guest_wait_avg']

			diff = no_alg_out['rest_time_finish'] - alg_out['rest_time_finish']
			diff2 = no_alg_out['guest_wait_avg'] - alg_out['guest_wait_avg']
			if diff < 0 or diff2 < 0:
				print "future guests: ", [k.name for k in copycopy_guests]
				print "future guests arrives: ", [k.arrive.seconds/60 for k in copycopy_guests]
				print "future guests orders: ", [k.orders for k in copycopy_guests]
				break

		data[rest_diff_col] = data[no_alg_col]-data[alg_col]
		data[rest_percent_col] = data[rest_diff_col]/data[no_alg_col]*100

		data[guest_diff_col] = data[no_alg_guest_avg_col]-data[alg_guest_avg_col]
		data[guest_percent_col] = data[guest_diff_col]/data[no_alg_guest_avg_col]*100

	data.to_csv(file_name, sep='\t', header=True, index=False)

def summarize_results_basic_size(sim_num, file_name):
	pd.set_option('display.width', 99999)
	pd.set_option('display.max_rows', 400)

	data = pd.read_csv(file_name, sep = '\t')
	data_summarize = pd.DataFrame()

	rest_wait_avgs = []
	guest_wait_avgs = []

	for i in range(sim_num):
		rest_case_avg = data.iloc[:,5+i*8].sum()/len(data.index)
		rest_wait_avgs.append(rest_case_avg)
		guest_case_avg = data.iloc[:,7+i*8].sum()/len(data.index)
		guest_wait_avgs.append(guest_case_avg)

	data_summarize['rest_wait_avgs'] = rest_wait_avgs
	data_summarize['guest_wait_avgs'] = guest_wait_avgs

	summarize_file_name = "sim_summarize.txt"

	data_summarize.to_csv(summarize_file_name, sep='\t', header=True, index=False)

	print rest_wait_avgs
	print guest_wait_avgs


def simulate_basic_max_eta(eta_max, sample_num, max_cust, file_name):
	data = pd.DataFrame()

	sim_num = int(eta_max/1)

	for i in range(sim_num):
		print i
		for j in range(sample_num):
			sample_eta = .1 + .1*sim_num
			rest = restaurant.Restaurant()
			chf = chef.Chef(idn = "aaron")
			rest.chefs.append(chf)
			copy_guests = []

			future_guests = sg.create_guests(n=max_cust, p_eta=sample_eta, p_order=4)
			sg.copy_guests(future_guests, copy_guests)

			# Compare with the algorithm
			alg_out = algorithm_time(future_guests, rest)

			# Compare with the no_algorithm
			no_alg_out = no_algorithm_time(copy_guests, rest)

			alg_col = 'alg_rest'+str(i)
			no_alg_col ='no_alg_rest'+str(i)
			rest_diff_col = 'rest_diff'+str(i)
			rest_percent_col = 'rest_diff_percent'+str(i)

			alg_guest_avg_col = 'alg_guest_wait_avg'+str(i)
			no_alg_guest_avg_col = 'no_alg_guest_wait_avg'+str(i)
			guest_diff_col = 'guest_diff'+str(i)
			guest_percent_col = 'guest_diff_percent'+str(i)

			data.loc[j,alg_col] = alg_out['rest_time_finish']
			data.loc[j,no_alg_col] = no_alg_out['rest_time_finish']

			data.loc[j,alg_guest_avg_col] = alg_out['guest_wait_avg']
			data.loc[j,no_alg_guest_avg_col] = no_alg_out['guest_wait_avg']

		data[rest_diff_col] = data[no_alg_col]-data[alg_col]
		data[rest_percent_col] = data[rest_diff_col]/data[no_alg_col]*100

		data[guest_diff_col] = data[no_alg_guest_avg_col]-data[alg_guest_avg_col]
		data[guest_percent_col] = data[guest_diff_col]/data[no_alg_guest_avg_col]*100

	data.to_csv(file_name, sep='\t', header=True, index=False)



if __name__ == "__main__":

	# Create restaurant, chef, and customer objects
	restaurant = restaurant.Restaurant()
	chef = chef.Chef(idn = "aaron")
	restaurant.chefs.append(chef)
	copy_guests = []

	future_guests = sg.create_guests(mode = 'case_1')
	# future_guests = sg.create_guests(n=5)
	sg.copy_guests(future_guests, copy_guests)

	# print "guests: ", [g.name for g in future_guests]
	# print "arrive: ", [g.arrive.seconds/60 for g in future_guests]
	# print "orders: ", [g.orders for g in future_guests]

	# Compare with the algorithm
	alg_count = algorithm_time(future_guests, restaurant)
	
	# Compare with the no_algorithm
	no_alg_count = no_algorithm_time(copy_guests, restaurant)

	print alg_count
	print no_alg_count

	# sim_num = 20
	# sample_num = 1000
	# file_name = 'alg_1c0t_sim_guestsize.txt'
	# simulate_basic_max_cust_size(sim_num, sample_num, file_name)
	# summarize_results_basic_size(sim_num, file_name)

	# sample_num = 500
	# eta_max = 30
	# max_cust = 20
	# sim_num = int(eta_max/1)
	# file_name = 'alg_1c0t_sim.txt'
	# simulate_basic_max_eta(eta_max, sample_num, max_cust, file_name)
	# summarize_results_basic_size(sim_num, file_name)


	
	

	
		

	













