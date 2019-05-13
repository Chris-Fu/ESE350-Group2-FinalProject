import time, serial, datetime, msvcrt, Modules
import keyboard
import statistics as st

__version__ = '20190429'
product_ID = '0D28:0204'
_instances = [] # store RTBox instances


def keyboard_sim_delay(ser):
	nTrials = 30
	print("BEGINNING OFFSET CALCULATION. DO NOT STOP SCRIPT MIDWAY.\r\n")
	print("Conducting " + str(nTrials) + " trials...")
	
	while 1:
		ser.write(b'i') # sends out initialization  pulse
		if msvcrt.getch() == 'i':
			print("Communication with MBED successful!")
			ser.write(b'k')
			break
		else:
			time.sleep(1)
			pass   
	
	# FIRST determine serial latency
	round_trips = []
	print("SENDING PINGS")
	time.sleep(3)
	for i in range(nTrials):
		ser.write(b'p')  # sends out pulse
		time_a = time.time()
		print(time_a)
		if ser.read(1) == 'p': # when mbed pings back
			round_trip = (time.time() - time_a) / 2
			#print(round_trip * 1000000)
			round_trips.append(round_trip * 1000000)
		time.sleep(0.25)
	serial_latency = st.mean(round_trips)
	serial_latency_std = st.stdev(round_trips)
	
	print(serial_latency)
	print(serial_latency_std)
	time.sleep(2)

    # SECOND find round trip with usb
	usb_trips = []
	print("SENDING PULSES")
	for i in range(nTrials):
		ser.write(b'p')  # sends out pulse
		time_a = time.time()
		if msvcrt.getch() == ' ':
			round_trip = time.time() - time_a
			usb_trips.append((round_trip * 1000000) - serial_latency)
		time.sleep(0.25)
	usb_latency = st.mean(usb_trips)
	usb_latency_std = st.stdev(usb_trips)
	
	print(usb_latency)
	print(usb_latency_std)
	time.sleep(2)

    # SENDS TO MICROCONTROLLER
	print("SENDING TO MBED")
	if ser.read(1) == 'r':
		ser.write("%f\n".format(str(serial_latency)).encode())
	if ser.read(1) == 'r':
		ser.write("%f\n".format(str(serial_latency_std)).encode())
	if ser.read(1) == 'r':
		ser.write("%f\n".format(str(usb_latency)).encode())
	if ser.read(1) == 'r':
		ser.write("%f\n".format(str(usb_latency_std)).encode())

	return serial_latency, serial_latency_std, usb_latency, usb_latency_std


