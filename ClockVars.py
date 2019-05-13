import time, serial, datetime, Modules


def clock_ratio(ser):
    nTrials = 30

    print("BEGINNING PTP CLOCK SYNCING PROTOCOL. DO NOT STOP SCRIPT MIDWAY.\r\n")
    print("Conducting " + str(nTrials) + " sync trials...")

    while 1:
        ser.write(b'i') # sends out initialization  pulse
        time.sleep(1)
        if ser.read(1) == 'i':
            print("Communication with MBED successful!")
            break
        else:
            time.sleep(1)

    pulse_times = []
    print("SENDING PULSES")
    for i in range(nTrials):
        t1_1 = time.time() * 1000000
        ser.write(b'p') # sends out pulse
        t1_2 = time.time() * 1000000

        pulse_times.append((t1_1 + t1_2) / 2)
        time.sleep(0.25)

    time.sleep(2)
    ser.write(b'd') # notifies user that data is coming
    time.sleep(2)

    mbed_data = []
    print("RECEIVING DATA")
    for i in range(nTrials):
		mbed_data.append(float(ser.readline()))
		#print(mbed_data[i])

    if ser.read(1) == 'f':
		ratio = 0
		tDiff = 0
		tmbed = 0
		for k in range(0, nTrials - 1):
			ratio += (pulse_times[k + 1] - pulse_times[k]) / (mbed_data[k + 1] - mbed_data[k])
			tDiff += pulse_times[k] - mbed_data[k]
			tmbed += mbed_data[k]
		
		ratio = ratio / nTrials
		tDiff = tDiff / nTrials
		tmbed = tmbed / nTrials
		print("Clock Ratio is : " + str(ratio))
		print("Clock Difference is : " + str(tDiff))

		# SENDS TO MICROCONTROLLER
		print("SENDING DATA\r\n")
		if ser.read(1) == 'r':
			ser.write("%f\n".format(str(ratio)).encode())
		if ser.read(1) == 'r':
			ser.write("%f\n".format(str(tDiff)).encode())
		if ser.read(1) == 'r':
			ser.write("%f\n".format(str(tmbed)).encode())
			
		print("CLOCK VARIABLES COMPLETE!\r\n")
		return ratio, tDiff, tmbed

