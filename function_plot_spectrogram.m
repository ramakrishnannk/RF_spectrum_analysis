% This function plots the spectrogram
% [] = function_plot_spectrogram(time_array, freq_axis, spectrum_matrix, avg_len, title_text)
% where time_array is the full time axis
% freq_axis is the axis of frequency points
% spectrum_matrix is the matrix of spectrum power measurements
% avg_len is the decimation factor for the time axis
% title_text is the text to put on the title of the figure
function [] = function_plot_spectrogram(time_array, freq_axis, spectrum_matrix, avg_len, title_text, plot_num)
%Bismillahir Rahmanir Raheem
% Programmer: Tanim Taher
% Illinois Institute of Technology, Chicago, US
% Date: June 20, 2013
if avg_len==1
    spectrum_powers=spectrum_matrix;
    time_axis=time_array;
else

    spectrum_matrix=10.^(spectrum_matrix/10);
    t_points=floor(length(time_array)/avg_len);
    time_axis=time_array(1:avg_len:t_points*avg_len);
% t_points=length(time_axis);
    f_points=length(freq_axis);
    spectrum_powers=zeros(t_points,f_points);
    for t_i=1:t_points
        spectrum_powers(t_i,1:f_points)=mean(spectrum_matrix((t_i-1)*avg_len+1:t_i*avg_len,1:f_points));
    end
    spectrum_powers=10*log10(spectrum_powers);
end

figure(plot_num)
pcolor(freq_axis,time_axis,spectrum_powers)
ylabel('time in hours/day')
xlabel('Frequency (MHz)')
title(title_text)
shading flat
colorbar
