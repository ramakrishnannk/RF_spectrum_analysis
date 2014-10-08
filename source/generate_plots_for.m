function [duty_cycle] = generate_plots_for(freq_axis, all_time_offsetted, all_power, start_freq, stop_freq, start_period, stop_period, filepath)
    start_date = start_period(1:find(start_period == ' ') - 1);
    store_path = [filepath '\plots\from_' num2str(start_freq) '_to_' num2str(stop_freq) '\'];
    freq_index = find(freq_axis >= start_freq & freq_axis <= stop_freq);
    time_index = find(all_time_offsetted >= datenum(start_period) & all_time_offsetted <= datenum(stop_period));
    f_array = freq_axis(freq_index);
    time_array = all_time_offsetted(time_index);
    spectrum_array = all_power(time_index, freq_index);
    % Get noise floor and add margin to get threshold
    spectrum_array_one_dim = spectrum_array(:);
    [hist_vals, bins] = hist(spectrum_array_one_dim, (min(spectrum_array_one_dim) + (-10)):(max(spectrum_array_one_dim) + 10));
    noise_mean = bins(hist_vals == max(hist_vals));
    noise_mean_1 = mode(spectrum_array_one_dim);
    disp(['Noise floor selected for ' num2str(start_freq) ' to ' num2str(stop_freq) ' MHz band frequency range ' num2str(noise_mean)])
    disp(['Noise floor selected for ' num2str(start_freq) ' to ' num2str(stop_freq) ' MHz band frequency range ' num2str(noise_mean_1)])
    % Decide how much margin you want to give for each band plotted
    margin = 3;
    threshold = noise_mean + margin;
    % Plot Average, Minimum and Maximum power spectrum
    figure(1)
    plot(f_array, min(spectrum_array), 'g', f_array, mean(spectrum_array), 'b', f_array, max(spectrum_array), 'r')
    legend('Min power', 'Avg power', 'Max power')
    xlabel('Frequency in MHz')
    ylabel('Power in dBm')
    xlim([start_freq stop_freq])
    title(['Avg, min and max power-spectrum for ' num2str(start_freq) ' to ' num2str(stop_freq) ' MHz band from ' start_period ' to ' stop_period])
    % Plot Average power spectrum
    figure(2)
    plot(f_array, mean(spectrum_array), f_array, noise_mean, 'm', f_array, threshold, 'k')
    legend('Avg power', 'Noise Floor', 'Threshold')
    xlabel('Frequency in MHz')
    ylabel('Power in dBm')
    xlim([start_freq stop_freq])
    title(['Avg power-spectrum for ' num2str(start_freq) ' to ' num2str(stop_freq) ' MHz band with threshold ' num2str(noise_mean + margin) ' dBm'])
    % Spectrogram
    time_array_normalized = time_array - time_array(1);
    title_text = ['Spectrogram for ' num2str(start_freq) ' to ' num2str(stop_freq) ' MHz spectrum on ' start_date];
    function_plot_spectrogram(time_array_normalized, f_array, spectrum_array, 1, title_text, 3);
    figure(3)
    % ytick_sg = datestr(time_array_normalized, 'HH:MM');
    % disp(ytick_sg)
    % set(gca, 'YTickLabel', ytick_sg')
    % Duty-cycle plot
    duty_cycle = double(spectrum_array >= threshold);
    figure(4)
    plot(f_array, (sum(duty_cycle)/max(sum(duty_cycle)) * 100))
    xlabel('Frequency in MHz')
    ylabel('Occupancy %')
    xlim([start_freq stop_freq])
    title(['Duty cycle plot for ' num2str(start_freq) ' to ' num2str(stop_freq) ' MHz band from ' start_period ' to ' stop_period])
    status = exist(store_path, 'dir');
    if status == 0
        mkdir(store_path)
    end
    saveas(1, [store_path 'average_min_max_pwr_spectrum'], 'png');
    saveas(2, [store_path 'threshold_avg_pwr_spectrum'], 'png');
    saveas(3, [store_path 'spectrogram_plot'], 'png');
    saveas(4, [store_path 'duty_cycle_plot'], 'png');
    figure(5)
    hist(spectrum_array_one_dim, (min(spectrum_array_one_dim) + (-10)):(max(spectrum_array_one_dim) + 10))
    % clear start_freq stop_freq freq_index time_index spectrum_array time_array f_array
end