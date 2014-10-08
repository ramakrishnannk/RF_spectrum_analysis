#!/usr/bin/python

import os
import RFEye_spectrum_processor
from RFEye_spectrum_processor import config_reader
from RFEye_spectrum_processor import get_spectrum_data
import scipy.io as sio
# We are currently in source directory
pwd = os.getcwd()
os.chdir(RFEye_spectrum_processor.CODE_PATH)
dir_list = os.listdir()

# Start and stop "date time"
start_period = "08-27-2014 00:00:00"
stop_period = "08-27-2014 23:59:59"
# Start and stop frequency in MHz
start_freq = 88
stop_freq = 108
spec_data = get_spectrum_data(start_period, stop_period, start_freq, stop_freq)
# Save in MAT File to plot in MATLAB
matfile_name = str(start_freq) + "_" + str(stop_freq) + "_chicago_" + ".mat"
sio.savemat(matfile_name, {'time_array':spec_data.time_array, 'power_matrix':spec_data.power_matrix, 'f_array':spec_data.f_array})

# # Start and stop "date time"
# start_period = "08-27-2014 00:00:00"
# stop_period = "08-27-2014 23:59:59"
# # Start and stop frequency in MHz
# start_freq = 407
# stop_freq = 470
# spec_data = get_spectrum_data(start_period, stop_period, start_freq, stop_freq)
# # Save in MAT File to plot in MATLAB
# matfile_name = str(start_freq) + "_" + str(stop_freq) + ".mat"
# sio.savemat(matfile_name, {'time_array':spec_data.time_array, 'power_matrix':spec_data.power_matrix, 'f_array':spec_data.f_array})

# Start and stop "date time"
start_period = "08-27-2014 00:00:00"
stop_period = "08-27-2014 23:59:59"
# Start and stop frequency in MHz
start_freq = 698
stop_freq = 806
spec_data = get_spectrum_data(start_period, stop_period, start_freq, stop_freq)
# Save in MAT File to plot in MATLAB
matfile_name = str(start_freq) + "_" + str(stop_freq) + "_chicago_" + ".mat"
sio.savemat(matfile_name, {'time_array':spec_data.time_array, 'power_matrix':spec_data.power_matrix, 'f_array':spec_data.f_array})


# Start and stop "date time"
start_period = "08-27-2014 00:00:00"
stop_period = "08-27-2014 23:59:59"
# Start and stop frequency in MHz
start_freq = 2390
stop_freq = 2500
spec_data = get_spectrum_data(start_period, stop_period, start_freq, stop_freq)
# Save in MAT File to plot in MATLAB
matfile_name = str(start_freq) + "_" + str(stop_freq) + "_chicago_" + ".mat"
sio.savemat(matfile_name, {'time_array':spec_data.time_array, 'power_matrix':spec_data.power_matrix, 'f_array':spec_data.f_array})