#!/usr/bin/python

import os, datetime
import RFEye_spectrum_processor
from RFEye_spectrum_processor import config_reader
from RFEye_spectrum_processor import get_spectrum_data
import scipy.io as sio
# We are currently in source directory
pwd = os.getcwd()
os.chdir(RFEye_spectrum_processor.CODE_PATH)
dir_list = os.listdir()

start_band_list = [30, 57, 88, 108, 130, 174, 216, 265, 406, 470, 512, 608, 698, 806, 902, 928, 960]
stop_band_list = [57, 88, 108, 130, 174, 216, 265, 406, 470, 512, 608, 698, 806, 902, 928, 960, 1200]

start_band_list = [2200, 2300, 2360, 2390, 2500, 2686]
stop_band_list = [2300, 2360, 2390, 2500, 2686, 2900]

start_band_list = [108]
stop_band_list = [129.99]

assert len(start_band_list) == len(stop_band_list), "ERROR: start and stop band list frequencies don't match!"

for i in range(0, len(start_band_list)):
	# Start and stop "date time"
	start_period = "08-27-2014 00:00:00"
	stop_period = "08-27-2014 23:59:59"
	US_local_format = "%m-%d-%Y %H:%M:%S"
	yymmdd_HHMMSS_format = "%y%m%d_%H%M%S"
	# Start and stop frequency in MHz
	start_freq = start_band_list[i]
	stop_freq = stop_band_list[i]
	print("Start frequency is " + str(start_freq) + " MHz Stop frequency is " + str(stop_freq) + " MHz")
	spec_data = get_spectrum_data(start_period, stop_period, start_freq, stop_freq)
	start_period_in_yymmdd_HHMMSS = datetime.datetime.strptime(start_period, US_local_format).strftime(yymmdd_HHMMSS_format)
	stop_period_in_yymmdd_HHMMSS = datetime.datetime.strptime(stop_period, US_local_format).strftime(yymmdd_HHMMSS_format)
	# Save in MAT File to plot in MATLAB
	matfile_name = "RFEye_WiFiUS_Virginia_Tech_" + str(start_freq) + "-" + str(stop_freq) + "_" + start_period_in_yymmdd_HHMMSS + "-" + stop_period_in_yymmdd_HHMMSS + ".mat"
	sio.savemat(matfile_name, {'time_array':spec_data.time_array, 'power_matrix':spec_data.power_matrix, 'f_array':spec_data.f_array})
	
for i in range(0, len(start_band_list)):
	# Start and stop "date time"
	start_period = "08-30-2014 00:00:00"
	stop_period = "08-30-2014 23:59:59"
	US_local_format = "%m-%d-%Y %H:%M:%S"
	yymmdd_HHMMSS_format = "%y%m%d_%H%M%S"
	# Start and stop frequency in MHz
	start_freq = start_band_list[i]
	stop_freq = stop_band_list[i]
	print("Start frequency is " + str(start_freq) + " MHz Stop frequency is " + str(stop_freq) + " MHz")
	spec_data = get_spectrum_data(start_period, stop_period, start_freq, stop_freq)
	start_period_in_yymmdd_HHMMSS = datetime.datetime.strptime(start_period, US_local_format).strftime(yymmdd_HHMMSS_format)
	stop_period_in_yymmdd_HHMMSS = datetime.datetime.strptime(stop_period, US_local_format).strftime(yymmdd_HHMMSS_format)
	# Save in MAT File to plot in MATLAB
	matfile_name = "RFEye_WiFiUS_Virginia_Tech_" + str(start_freq) + "-" + str(stop_freq) + "_" + start_period_in_yymmdd_HHMMSS + "-" + stop_period_in_yymmdd_HHMMSS + ".mat"
	sio.savemat(matfile_name, {'time_array':spec_data.time_array, 'power_matrix':spec_data.power_matrix, 'f_array':spec_data.f_array})	