#!/bin/usr/python
import re, os, csv, datetime
import numpy as np
import pandas as pd
# Global declarations

global windows, linux, CODE_PATH
windows = 1
linux = 0

if windows:
	CODE_PATH = 'C:\\Users\\Vignesh\\Documents\\MATLAB\\MEng_Project'
elif linux:
	CODE_PATH = '/home/rk126/Documents/MATLAB/MEng_Project'

class config_reader:
	# start_freq = None
	# stop_freq = None
	# subfolder = None
	# filename = None
	def __init__(self, abs_filename):
		self.start_freq = []
		self.stop_freq = []
		self.subfolder = []
		self.filename = abs_filename
		self.read_config_file()
	def read_config_file(self):
		f = open(self.filename, 'r')
		for line in f:
			# Break when low resolution string is matched
			loop_breaker = re.search(r"""([Ll]ow)\s*[Rr]esolution""", line)
			if loop_breaker != None:
				# print(loop_breaker.group(0))
				break
			freq_match = re.search(r"""scan\s*=\s*\d+\w+,\s*\d+,\s*(\d+),\s*(\d+)""", line)
			if freq_match != None:
				# print(freq_match.group(0))
				self.start_freq.append(freq_match.group(1))
				self.stop_freq.append(freq_match.group(2))
			folder_match = re.search(r"""peak\d+\s*=\s*(\d+)""", line)
			if folder_match != None:
				# print(folder_match.group(0))
				self.subfolder.append(folder_match.group(1))
		f.close()

class get_spectrum_data:
	# cfg_data = None
	# start_period = None
	# stop_period = None
	# start_freq = None
	# stop_freq = None
	# files_to_read = None
	def __init__(self, start_period, stop_period, start_freq, stop_freq):
		# Assert that stop period is greater than or equal start period
		self.start_period = start_period
		self.stop_period = stop_period
		# Assert that the stop frequency is greater than the start frequency
		self.start_freq = start_freq
		self.stop_freq = stop_freq
		# Initialize time_array, f_array
		self.time_array = []
		self.f_array = []
		self.include_runs_dirs = []
		self.power_matrix = np.array([])
		self.first_entry = True
		# Read configuration file
		self.cfg_data = config_reader(CODE_PATH + '\\rfeyed.cfg')
		# Form the list of files to be read and filter out in terms of time and frequency
		self.list_files_to_read()
		# print(filtered_file_list)
		# count = 1
		# for filename in filtered_file_list:
		# 	print("File " + str(count) + " out of " + str(len(filtered_file_list)) + " going on")
		# 	self.read_csv_file(filename)
		# 	count += 1
		print(self.f_array.shape)
		print(self.power_matrix.shape)
		self.time_array = np.array(self.time_array)
		print(self.time_array.shape)
		# for datetime_each in self.time_array:
			# print(datetime_each)
		# for each_file in filtered_file_list:
			# self.get_freq_list(each_file)
		# Read each of the file and extract spectral data relevant to
		# frequency and period information parsed
		# for freq_list in self.f_array:
		# 	print(freq_list)
		
	def list_files_to_read(self):
		include_subfolders = False
		YYMMDD_list = []
		absolute_file_list = []
		# Prepare subfolders to read data from and also exclude 
		# those files which doesn't have the frequency listed
		# TODO, need to work on the logic of getting the list of folders
		for i in range(0, len(self.cfg_data.subfolder)):
			if int(self.cfg_data.start_freq[i]) <= self.start_freq and self.start_freq <= int(self.cfg_data.stop_freq[i]):
				include_subfolders = True
			if int(self.cfg_data.start_freq[i]) <= self.stop_freq and self.stop_freq <= int(self.cfg_data.stop_freq[i]):
				self.include_runs_dirs.append(self.cfg_data.subfolder[i])
				include_subfolders = False
			if include_subfolders:
				self.include_runs_dirs.append(self.cfg_data.subfolder[i])
		
		assert len(self.include_runs_dirs) != 0, "ERROR runs directory list to include is empty"
		# Split start_period/stop_period as start/stop date and start/stop time
		start_period_list = self.start_period.split(' ')
		stop_period_list = self.stop_period.split(' ')
		if start_period_list[0] == stop_period_list[0]:
			start_date = stop_date = start_period_list[0]
		else:
			start_date = start_period_list[0]
			stop_date = stop_period_list[0]
		start_date_in_YYMMDD = start_date[8:10] + start_date[0:2] + start_date[3:5]
		stop_date_in_YYMMDD = stop_date[8:10] + stop_date[0:2] + stop_date[3:5]
		directory_list = os.listdir(CODE_PATH + "\\Data")
		for date_dir_list in directory_list:
			# These subfolders are present in the Data directory, in directory with YYMMDD
			if  int(date_dir_list) >= int(start_date_in_YYMMDD):
				if int(date_dir_list) <= int(stop_date_in_YYMMDD):
					YYMMDD_list.append(date_dir_list)
		assert len(YYMMDD_list) != 0, "ERROR: List of YYMMDD folders to include is empty"
		for i in range(0, len(YYMMDD_list)):
			for j in range(0, len(self.include_runs_dirs)):
				dir_list = CODE_PATH + "\\Data\\" + YYMMDD_list[i] + "\\" + self.include_runs_dirs[j] + "\\" 
				for files in os.listdir(dir_list):
					match_csv = re.search(r"""\.csv""", files)
					if match_csv:
						absolute_file_list.append(dir_list + files)
		self.get_filtered_file_list(absolute_file_list)
		# Return filtered list of files
		# return self.get_filtered_file_list(absolute_file_list)
	
	def interpolate_gps_datetime(self, filename, unknown_index):
		GPSTimeDateRealTime = pd.read_csv(filename, usecols=['GPS_Time', 'GPS_Date', 'Time'])
		NumberOfRows = len(GPSTimeDateRealTime)
		gps_datetime_format = '%d/%m/%y %H:%M:%S'
		GPSDate = GPSTimeDateRealTime.loc[:, 'GPS_Date'].tolist()
		GPSTime = GPSTimeDateRealTime.loc[:, 'GPS_Time'].tolist()
		RealTime = GPSTimeDateRealTime.loc[:, 'Time'].tolist()
		if RealTime[unknown_index].count(':') == 2:
			real_time_format = "%H:%M:%S"
		elif RealTime[unknown_index].count(':') == 1:
			real_time_format = "%M:%S"
		go_up = False
		go_down = False
		if unknown_index <= (NumberOfRows/2):
			go_down = True
		else:
			go_up = True
		while (GPSDate[unknown_index] != "Unknown" or GPSTime[unknown_index] != "Unknown" or GPSDate[unknown_index] != "unknown" or GPSTime[unknown_index] != "unknown"):
			if not (unknown_index == 0 or unknown_index == (NumberOfRows - 1)):
				if go_up:
					if not (GPSDate[unknown_index - 1] == "Unknown" or GPSDate[unknown_index - 1] == "unknown" or GPSTime[unknown_index - 1] == "Unknown" or GPSTime[unknown_index - 1] == "unknown"):
						time_diff = datetime.datetime.strptime(RealTime[unknown_index].split('.').__getitem__(0), real_time_format) - datetime.datetime.strptime(RealTime[unknown_index - 1].split('.').__getitem__(0), real_time_format)
						interpolated_datetime_obj = datetime.datetime.strptime(GPSDate[unknown_index - 1] + ' ' + GPSTime[unknown_index - 1], "%d/%m/%y %H:%M:%S") + time_diff
						return interpolated_datetime_obj.strftime(gps_datetime_format)
					else:
						GPSDateTime = self.interpolate_gps_datetime(filename, unknown_index - 1).split(' ')
						GPSDate[unknown_index - 1] = GPSDateTime[0]
						GPSTime[unknown_index - 1] = GPSDateTime[1]
						
				if go_down:
					if not (GPSDate[unknown_index + 1] == "Unknown" or GPSDate[unknown_index + 1] == "unknown" or GPSTime[unknown_index + 1] == "Unknown" or GPSTime[unknown_index + 1] == "unknown"):
						time_diff = datetime.datetime.strptime(RealTime[unknown_index + 1].split('.').__getitem__(0), real_time_format) - datetime.datetime.strptime(RealTime[unknown_index].split('.').__getitem__(0), real_time_format)
						interpolated_datetime_obj = datetime.datetime.strptime(GPSDate[unknown_index + 1] + ' ' + GPSTime[unknown_index + 1], "%d/%m/%y %H:%M:%S") - time_diff
						return interpolated_datetime_obj.strftime(gps_datetime_format)
					else:
						GPSDateTime = self.interpolate_gps_datetime(filename, unknown_index + 1).split(' ')
						GPSDate[unknown_index + 1] = GPSDateTime[0]
						GPSTime[unknown_index + 1] = GPSDateTime[1]
						
			elif unknown_index == 0:
				go_up = False
				go_down = True
				if not (GPSDate[unknown_index + 1] == "Unknown" or GPSDate[unknown_index + 1] == "unknown" or GPSTime[unknown_index + 1] == "Unknown" or GPSTime[unknown_index + 1] == "unknown"):
					time_diff = datetime.datetime.strptime(RealTime[unknown_index + 1].split('.').__getitem__(0), real_time_format) - datetime.datetime.strptime(RealTime[unknown_index].split('.').__getitem__(0), real_time_format)
					interpolated_datetime_obj = datetime.datetime.strptime(GPSDate[unknown_index + 1] + ' ' + GPSTime[unknown_index + 1], "%d/%m/%y %H:%M:%S") - time_diff
					return interpolated_datetime_obj.strftime(gps_datetime_format)
				else:
					GPSDateTime = self.interpolate_gps_datetime(filename, unknown_index + 1).split(' ')
					GPSDate[unknown_index + 1] = GPSDateTime[0]
					GPSTime[unknown_index + 1] = GPSDateTime[1]
					
			elif unknown_index == (NumberOfRows - 1):
				go_up = True
				go_down = False
				if not (GPSDate[unknown_index - 1] == "Unknown" or GPSDate[unknown_index - 1] == "unknown" or GPSTime[unknown_index - 1] == "Unknown" or GPSTime[unknown_index - 1] == "unknown"):
					time_diff = datetime.datetime.strptime(RealTime[unknown_index].split('.').__getitem__(0), real_time_format) - datetime.datetime.strptime(RealTime[unknown_index - 1].split('.').__getitem__(0), real_time_format)
					interpolated_datetime_obj = datetime.datetime.strptime(GPSDate[unknown_index - 1] + ' ' + GPSTime[unknown_index - 1], "%d/%m/%y %H:%M:%S") + time_diff
					return interpolated_datetime_obj.strftime(gps_datetime_format)
				else:
					GPSDateTime = self.interpolate_gps_datetime(filename, unknown_index - 1).split(' ')
					GPSDate[unknown_index - 1] = GPSDateTime[0]
					GPSTime[unknown_index - 1] = GPSDateTime[1]
		
	def get_filtered_file_list(self, absolute_file_list):
		# Get the file list to be read completely segregating in accordance with the start and stop period
		filtered_file_list = []
		file_count = 1
		for file in absolute_file_list:
			GPSTimeDateRealTime = pd.read_csv(file, usecols=['GPS_Time', 'GPS_Date', 'Time'])
			NumberOfRows = len(GPSTimeDateRealTime)
			GPSDate = GPSTimeDateRealTime.loc[:, 'GPS_Date'].tolist()
			GPSTime = GPSTimeDateRealTime.loc[:, 'GPS_Time'].tolist()
			RealTime = GPSTimeDateRealTime.loc[:, 'Time'].tolist()
			count = 0
			for i in range(0, NumberOfRows):
				if not (GPSDate[i] == "Unknown" or GPSDate[i] == "unknown" or GPSTime[i] == "Unknown" or GPSTime[i] == "unknown"):
					gps_datetime = GPSDate[i] + ' ' + GPSTime[i]
				else:
					# Interpolating unknown date time point
					gps_datetime = self.interpolate_gps_datetime(file, i)
				gps_datetime_format = "%d/%m/%y %H:%M:%S"
				US_datetime_format = "%m-%d-%Y %H:%M:%S"
				local_datetime_str = self.add_offset(gps_datetime, gps_datetime_format, '-0400')
				local_datetime_MATLAB_datenum = self.datetime_str_to_MATLAB_datenum(local_datetime_str, gps_datetime_format)
				start_period_MATLAB_datenum = self.datetime_str_to_MATLAB_datenum(self.start_period, US_datetime_format)
				stop_period_MATLAB_datenum = self.datetime_str_to_MATLAB_datenum(self.stop_period, US_datetime_format)
				if start_period_MATLAB_datenum <= local_datetime_MATLAB_datenum and local_datetime_MATLAB_datenum <= stop_period_MATLAB_datenum:
					self.time_array.append(local_datetime_MATLAB_datenum)
					count += 1
			if count > 0:
				print(count)
				print("File Number " + str(file_count) + " going on")
				file_count += 1
				self.read_csv_file(file)
				# filtered_file_list.append(file)
		# return filtered_file_list
	
	# def get_freq_list(self, filename):
		# print("In Freq list function")
		# for subfolders in self.include_runs_dirs:
			# match = re.search(subfolders, filename)
			# if match != None:
				
		
		# # Read the CSV file once more to get the frequency information
		# first_two_rows = pd.read_csv(filename, nrows = 1)
		# start_freq_in_file = int(first_two_rows.get_value(0, "Start_Frequency"))
		# stop_freq_in_file = int(first_two_rows.get_value(0, "End_Frequency"))
		# # Check if user specified start frequencies and stop frequencies correspond to one in the file
		# if self.start_freq >= start_freq_in_file and self.stop_freq <= stop_freq_in_file:
			# print("start_freq and stop_freq within the file limits")
		# else:
			# return
		# # Check if f_array has these bounds, if yes return None if no return updated f_array
		# if len(self.f_array) != 0:
			# if self.start_freq >= min(self.f_array) and self.stop_freq <= max(self.f_array):
				# print("No need to update")
				# return
			# else:
				# print("Need to update")
		
		# frequency_list_in_file = first_two_rows.columns.tolist()
		# frequency_list_in_file = frequency_list_in_file[frequency_list_in_file.index(str(start_freq_in_file)):(len(frequency_list_in_file) - 1)]
		# for_count = 0
		# for frequencies in frequency_list_in_file:
			# print("in for loop")
			# print(for_count)
			# for_count += 1
			# if self.start_freq <= np.float64(frequencies) and np.float64(frequencies) <= self.stop_freq:
				# if len(self.f_array) == 0:
					# self.f_array.append(np.float64(frequencies))
				# else:
					# # Check if frequency already in the list
					# if frequencies not in self.f_array:
						# self.f_array.append(np.float64(frequencies))
	
	def add_offset(self, datetime_str, datetime_format, offset):
		datetime_obj = datetime.datetime.strptime(datetime_str, datetime_format)
		offset_obj = datetime.datetime.strptime('+0000', '%z') - datetime.datetime.strptime(offset, "%z")
		datetime_offsetted = datetime_obj + offset_obj
		return datetime_offsetted.strftime(datetime_format)
	
	def datetime_str_to_MATLAB_datenum(self, date_time, datetime_format):
		""" Arguments - tuple of form (date, time), date_format dd/mm/yy or mm-dd-yyyy
			Returns - datenum with standard date/time string tuples
		"""
		datetime_obj = datetime.datetime.strptime(date_time, datetime_format)
		frac = (datetime_obj - datetime.datetime(datetime_obj.year, datetime_obj.month, datetime_obj.day, 0, 0, 0)).seconds / (24.0 * 60.0 * 60.0)
		MATLAB_datenum_format = (datetime_obj + datetime.timedelta(days = 366)).toordinal() + frac
		return MATLAB_datenum_format
	
	# Convert datetime_str to MATLAB's datenum which can be used for comparisons
	def MATLAB_datenum_to_str(self, datenum_time_date):
		""" Arguments - datenum_time_date
		Returns - Date Time string of format mm-dd-yyyy HH:MM:SS
		"""
		matlab_datenum = datenum_time_date
		python_datetime = datetime.datetime.fromordinal(int(matlab_datenum)) + datetime.timedelta(days=matlab_datenum%1) - datetime.timedelta(days = 366)
		return python_datetime.strftime("%m-%d-%y %H:%M:%S")
		
	# def read_csv_file(self, filename):
		# freq_list = pd.read_csv(filename, nrows=1).columns.tolist()
		# freq_list_float = []
		# for subdir in self.include_runs_dirs:
			# if re.search(subdir, filename):
				# Find start_freq
				# start_freq_in_file = self.cfg_data.start_freq[self.cfg_data.subfolder.index(subdir)]
		# start_freq_index = freq_list.index(str(start_freq_in_file))
		# for freq in freq_list[start_freq_index:]:
			# if freq.count('.') == 1:
				# freq_list_float.append(np.float64(freq))
			# elif freq.count('.') == 2:
				# freq_list_float.append(np.float64(re.match(r"""(\d+.\d+).\d+""", freq).group(1)))
		# freq_list_float
		
	def read_csv_file(self, filename):
		freq_list = pd.read_csv(filename, nrows=1).columns.tolist()
		freq_list_float = []
		for subdir in self.include_runs_dirs:
			if re.search(subdir, filename):
				# Find start_frequency in each running file
				start_freq_in_file = self.cfg_data.start_freq[self.cfg_data.subfolder.index(subdir)]
				start_freq_index = freq_list.index(str(start_freq_in_file))
				for freq in freq_list[start_freq_index:]:
					if freq.count('.') == 0:
						if freq.isdigit():
							freq_list_float.append(np.float64(freq))
					elif freq.count('.') == 1:
						freq_list_float.append(np.float64(freq))
					elif freq.count('.') == 2:
						freq_list_float.append(np.float64(re.match(r"""(\d+.\d+).\d+""", freq).group(1)))
		np_freq_list_float = np.array(freq_list_float)
		first_index = start_freq_index + min((np.where(np_freq_list_float >= self.start_freq))[0])
		last_index = start_freq_index + max((np.where(np_freq_list_float <= self.stop_freq))[0])
		columns = freq_list[first_index:last_index]
		spectrum_array = pd.read_csv(filename, usecols=columns).values    
		if self.first_entry:
			self.first_entry = False
			self.power_matrix = spectrum_array
		else:
			self.power_matrix = np.concatenate((self.power_matrix, spectrum_array), axis=0)
		self.f_array = np.array(freq_list_float[(first_index - start_freq_index):(last_index - start_freq_index)])
		# Return f_array, spectrum_array and time_array