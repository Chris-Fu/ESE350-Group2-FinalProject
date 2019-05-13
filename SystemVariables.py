import ClockVars, USBLatency, Modules, time, msvcrt
from datetime import datetime
import numpy as np

if __name__ == "__main__":
    ser = Modules._openPort()
    sys_vars_filename = "test-sysvars"

    device_name = "YOYOYO"
    calibration = "Keyboard"
    curr_time = datetime.utcnow()

    sys_vars = []

    while 1:
		ser.write(b'V') # sends out clock ratio mode
		time.sleep(1)
		print("attempting to start...")
		check = ser.read(1)
		if check == 'V':
			print("Mbed set to Clock Ratio Mode!")
			time.sleep(3)
			break
		else:
			print("cant start...")
			time.sleep(1)
    clkratio, tdiff, tmbed = ClockVars.clock_ratio(ser)
    sys_vars.append(clkratio)
    sys_vars.append(tdiff)
    sys_vars.append(tmbed)

    time.sleep(5) # chills for a second, waiting for mbed to respond

    while 1:
        ser.write(b'U') # sends out latency mode
        time.sleep(1)
        if ser.read(1) == 'U':
            print("Mbed set to USB Latency Mode!")
            time.sleep(3)
            break
        else:
            time.sleep(1)
    serial_latency, serial_latency_std, usb_latency, usb_latency_std = USBLatency.keyboard_sim_delay(ser)
    sys_vars.append(serial_latency)
    sys_vars.append(serial_latency_std)
    sys_vars.append(usb_latency)
    sys_vars.append(usb_latency_std)

    Modules.export_helper(sys_vars_filename, device_name, calibration, curr_time, np.asarray(sys_vars))
