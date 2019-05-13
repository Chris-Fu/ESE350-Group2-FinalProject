"""
"""
from Modules import *

if __name__ == "__main__":
	ser = Modules._openPort()
    sys_vars_filename = "SDFSDF"
    results_filename = "YEYEYE"
    screen_filename = "YAYY"
    keyboard_filename = "OKAAAAAAY"

    cognition_filename = "HAHAHA"
    calculation_filename = "SDSDSDSD"

    device_name = "YOYOYO"
    calibration = "Keyboard"
    curr_time = datetime.utcnow();

    sys_vars = result_data_extract(sys_vars_filename)
    clkratio = sys_vars[0]
    tdiff = sys_vars[1]
    tmbed = sys_vars[2]
	tStart = sys_vars[3]
    serial_latency = sys_vars[4]
    serial_latency_std = sys_vars[5]
    usb_latency = sys_vars[6]
    usb_latency_std = sys_vars[7]
	
	# IF I EVER GET THE MBED TO LOG THE DATA SOMEWHERE...
	# sys_vars[8]
	# ser.write(b'S') # tells mbed to send all possible data
	# time.sleep(1);
	# if ser.read(1) == 'S':
		# sys_vars[0] = ser.readline(); # clkratio
		# sys_vars[1] = ser.readline(); # tdiff
		# sys_vars[2] = ser.readline(); # tmbed
		# sys_vars[3] = ser.readline(); # tStart
		# sys_vars[4] = ser.readline(); # serialLatency
		# sys_vars[5] = ser.readline(); # serialLatencySTD
		# sys_vars[6] = ser.readline(); # USBlatency
		# sys_vars[7] = ser.readline(); # USBlatencySTD

    detect = result_data_extract(results_filename)
    screen = result_data_extract(screen_filename)
    keyboard = result_data_extract(keyboard_filename)

    cognition, present, response = \
        cognition_data_extract(cognition_filename)[0:len(detect)] # caps at length of results


    results = []
    screen_results = []
    keyboard_results = []
    for i in range(len(detect)):
        os_delay = cognition[i] - detect[i]
        screen_delay = present[i] - toComputerTime(sys_vars, screen[i]) #TODO: convert between clock times
        keyboard_delay = response[i] - toComputerTime(sys_vars, keyboard[i])

        if detect[i] < 0 or os_delay > 5.0 or os_delay < 0.0:
            continue

        results.append(os_delay)
        screen_results.append(screen_delay)
        keyboard_results.append(keyboard_delay)

    export_helper(calculation_filename, device_name, calibration, curr_time, results)


    print("COMPLETED CALCULATION. EXITING...")
