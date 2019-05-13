"""
    Author: Christopher Fu

    Purpose:
    Modules to help Tests.py and Mbed.py
"""
import time, serial, msvcrt, os
import numpy as np
from datetime import datetime

__version__ = '20190429'
product_ID = '0D28:0204'
_instances = [] # store RTBox instances


def _openPort():
    #print("ATTEMPTING SERIAL CONNECTION...")
    from serial.tools.list_ports import comports
    try:
        import fcntl  # take care of multiple open in unix
    except:
        pass

    inUse = []  # for error message
    for box in _instances: inUse.append(box._ser.port)
    for p in comports():
        try:
            # p has ['COM4', 'USB Serial Port (COM4)', 'USB VID:PID=0403:6001 SER=6']
            if p[0] in inUse or 'USB' not in p[2] or product_ID not in p[2]: continue
            ser = serial.Serial(p[0], 115200, timeout=5.0)

            if 'fcntl' in locals():
                try:  # PTB ioctl(TIOCEXCL) the same as this?
                    fcntl.flock(ser.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                except IOError:  # already in use
                    ser.close()  # buffer cleared when open, not ideal
                    raise serial.SerialException(p[0] + ' in use')  # record inUse

            # print("CONNECTION TO " + str(p[0]) + " SUCCESSFUL!")
            return ser
        except:
            inUse.append(p[0])  # normally denied access

    # if not return yet, get some useful error info
    if len(inUse) == 0:
        err = 'No RTBox serial port found. Make sure FTDI driver is installed, or check product ID'
    elif len(inUse) == 1:
        err = 'Possible RTBox port %s is already in use' % inUse[0]
    else:
        err = 'Possible RTBox ports %s are already in use' % inUse
    raise serial.SerialException("FUCKKKKKKKKKK")


def toComputerTime(sys_vars, value):
	clkratio = sys_vars[0]
	tdiff = sys_vars[1]
	tmbed = sys_vars[2]
	tStart = sys_vars[3]
	serial_latency = sys_vars[4]
	serial_latency_std = sys_vars[5]
	usb_latency = sys_vars[6]
	usb_latency_std = sys_vars[7]
	
	return ((value - tmbed) * clkratio) + tmbed + tdiff


def write_row(file, data):
    for line in data:
        line = str(line)
        file.write(line)
        file.write(',')
    file.write('\n')


def export_helper(filename, device_name, calibration, curr_time, results):
    mean = np.nanmean(results)
    std = np.nanstd(results)
    max = np.nanmax(results)
    median = np.nanmedian(results)
    min = np.nanmin(results)
    range = max - min

    export_vals = []
    export_vals.append(device_name)
    export_vals.append(calibration)
    export_vals.append(str(mean))
    export_vals.append(str(std))
    export_vals.append(str(max))
    export_vals.append(str(median))
    export_vals.append(str(min))
    export_vals.append(str(range))
    export_vals.append(curr_time)

    export_headers = ["name", "calibration", "mean", "std", "max", "median", "min", "range", "start_time"]

    try:
        os.mkdir("results/")
    except:
        wow = 1
    filename = filename + ".csv"
    file = open("results/" + filename, "w+")
    write_row(file, export_headers)
    write_row(file, export_vals)
    write_row(file, ["\n", "ALL DATA:"])
    write_row(file, results)
    file.close()
    print("Export Successful!")


def result_data_extract(filename):
    if (filename[len(filename) - 4:] == ".csv"):
        pass
    else:
        filename = filename + ".csv"

    try:
        file = open(os.getcwd() + "/results/" + filename, 'r')

        file.readline()
        second_line = file.readline()
        calibration = second_line.split(',')[1]
        file.readline()
        file.readline()

        data = file.readline().split(',')
        detect_data = []
        for datapoint in data:
            if datapoint.strip() == "":
                break
            detect_data.append(float(datapoint))

        file.close()

        print("Data extraction successful!")
        return detect_data
    except:
        print("Could not find results file.")
        quit()


def cognition_data_extract(filename):
    if filename[len(filename) - 4:] == ".csv":
        pass
    else:
        filename = filename + ".csv"

    try:
        file = open(os.getcwd() + "/psychomotor/" + filename, 'r')
        cognition_data = []
        present_data = []
        response_data = []

        while True:
            presented_line = file.readline()
            presented = presented_line.split(',')

            if len(presented) < 3:
                continue
            if presented[3] == '"TaskStopped"' or presented[3] == 'TaskStopped':
                break
            if not(presented[3] == '"StimulusPresented"') or \
                    not(presented[3] == 'StimulusPresented'):
                continue

            present_time = float(presented[2][1:len(presented[2]) - 1])
            present_data.append(present_time)

            response_line = file.readline()
            response_time = float(response_line[2][1:len(response_line[2]) - 1])
            response_data.append(response_time)

            total_time = response_time - present_time
            cognition_data.append(total_time)

        file.close()

        print("Data extraction successful!")
        return cognition_data, present_data, response_data
    except:
        print("Could not find cognition file.")
        quit()

