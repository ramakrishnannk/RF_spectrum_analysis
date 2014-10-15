filepath = pwd;
file_list = ls(filepath);
[row_len, ~] = size(file_list);
mean_duty_cycle = [];
for i = 1:row_len
    if ~isequal(strfind(file_list(i, :), '.mat'), [])
        disp(file_list(i, :))
        load(file_list(i, :))
        start_freq = f_array(1);
        stop_freq = round(f_array(end));
        start_period = datestr(time_array(1));
        stop_period = datestr(time_array(end));
        mean_duty_cycle = [mean_duty_cycle generate_plots_for(f_array, time_array, power_matrix, start_freq, stop_freq, start_period, stop_period, filepath, 3)];
    end
    clear f_array time_array power_matrix
end