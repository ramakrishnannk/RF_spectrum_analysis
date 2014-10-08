start_freq_list = [30, 130, 650, 1200, 3000]
stop_freq_list = [130, 698, 1200, 3000, 6000]
start_freq = 450
stop_freq = 1500
subfolders = [11, 12, 13, 14, 15]
subfolders_rev = []
include_subfolders = False

for i in range(0, len(subfolders)):
	if start_freq_list[i] <= start_freq and start_freq <= stop_freq_list[i]:
		include_subfolders = True
	if start_freq_list[i] <= stop_freq and stop_freq <= stop_freq_list[i]:
		subfolders_rev.append(subfolders[i])
		include_subfolders = False
	if include_subfolders:
		subfolders_rev.append(subfolders[i])

print(subfolders_rev)