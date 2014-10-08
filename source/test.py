from RFEye_spectrum_processor import get_spectrum_data

start_period = "08-26-2014 00:00:00"
stop_period = "08-27-2014 07:34:25"
# Start and stop frequency in MHz
start_freq = 35
stop_freq = 60
spec_data = get_spectrum_data(start_period, stop_period, start_freq, stop_freq)
time_date_tuple = stop_period.split(' ')
time_date_tuple = (time_date_tuple[0], time_date_tuple[1])
date_format = 'mm-dd-yyyy'
tuple_format = spec_data.datetime_to_MATLAB_datenum(time_date_tuple, date_format)
print(spec_data.add_offset(tuple_format[0], '-04:00'))