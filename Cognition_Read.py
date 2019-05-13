import Modules, time, msvcrt
from datetime import datetime
import numpy as np


def cognition_read(ser):
	print("\n\nPlease reset the MBED controller.\r\nOnce the LEDs turn on, hit spacebar on this computer to"
		  "start Cognition;\r\n")
	should_export = True

	primed = False
	light_prime = False
	touch_prime = False
	check_state = False

	light_temp = -1
	touch_temp = -1

	light_data = []
	touch_data = []
	diff_data = []

	# waits for spacebar hit to initiate cognition
	while 1:
		if msvcrt.kbhit():
			if msvcrt.getch() == ' ':
				ser.write(b'i')
				print("Sending start command. Should start cognition.\r\n")
				tStart = float(ser.readline())
				print("Recieved mbed start time as " + str(tStart))
				break

	while 1:
		if msvcrt.kbhit():
			user_input = msvcrt.getch()
			if user_input == 'q':
				ser.write(b'q')
				print("Received quit command! Quitting and exporting...\r\n")
				break
			if user_input == 'x':
				ser.write(b'q')
				print("Received quit command with no export! Quitting...\r\n")
				should_export = False
				break

		input = ser.readline().upper()
		if len(input) == 0:
			continue
		#print(input)

		if primed:
			input_split = input.split('.')
			if len(input_split) == 2: # doesn't actually capture anything
				input = input_split[0]
			primed = False

			if light_prime:
				light_prime = False
				light_temp = int(input)
				#print("PRESS SPACEBAR\r\n")
			if touch_prime:
				touch_prime = False
				touch_temp = int(input)
				# print("Recieved touch results. Checking if valid...\r\n")
			if check_state:
				check_state = False
				if light_temp < 0 or touch_temp < 0:
					print("ERROR OCCURRED DURING DATA COLLECTION! DISCARDING MOST RECENT DATAPOINT...\r\n")
				else:
					# print("Successful Capture! Saving values...\r\n")
					light_data.append(light_temp)
					touch_data.append(touch_temp)
					diff_data.append(touch_temp - light_temp)

				light_temp = -1.0
				touch_temp = -1.0

		if input[0] == "L":
			light_prime = True
		if input[0] == "T" or input[0] == "S":
			if light_temp < 0:
				print("Pressed spacebar before system was ready. Please try again...\r\n")
			else:
				touch_prime = True
		if input[0] == "C":
			check_state = True
		if input[0] == "I":
			print("Recieved quit command! Quitting...\r\n")
			break

		primed = light_prime or touch_prime or check_state

	print(light_data)
	print(touch_data)
	print(diff_data)

	return light_data, touch_data, diff_data, should_export, tStart


if __name__ == "__main__":
	ser = Modules._openPort()
	while 1:
		ser.write(b'C') # sends out clock ratio mode
		time.sleep(1)
		print("attempting to start...")
		check = ser.read(1)
		if check == 'C':
			print("Mbed set to Clock Ratio Mode!")
			time.sleep(3)
			break
		else:
			print("cant start...")
			time.sleep(1)
	# PARAMETERS. Please change this to send values
	sys_vars_filename = "SDFSDF"
	full_delay_filename = "test-all"
	screen_delay_filename = "test-screen"
	keyboard_delay_filename = "test-keyboard"
	sys_vars_filename = "test-sysvars"

	device_name = "YOYOYO"
	calibration = "Keyboard"
	curr_time = datetime.utcnow()

	light_data, touch_data, diff_data, should_export, tStart = cognition_read(ser)

	sys_vars = result_data_extract(sys_vars_filename)
	new_sys_vars[0] = sys_vars[0]
	new_sys_vars[1] = sys_vars[1]
	new_sys_vars[2] = sys_vars[2]
	new_sys_vars[3] = tStart
	new_sys_vars[4] = sys_vars[3]
	new_sys_vars[5] = sys_vars[4]
	new_sys_vars[6] = sys_vars[5]
	new_sys_vars[7] = sys_vars[6]
	Modules.export_helper(sys_vars_filename, device_name, calibration, curr_time, np.asarray(new_sys_vars))

	if should_export:
		Modules.export_helper(full_delay_filename, device_name, calibration, curr_time, np.asarray(diff_data))
		Modules.export_helper(screen_delay_filename, device_name, calibration, curr_time, np.asarray(light_data))
		Modules.export_helper(keyboard_delay_filename, device_name, calibration, curr_time, np.asarray(touch_data))

	print("COMPLETED COGNITION READ. EXITING...")
