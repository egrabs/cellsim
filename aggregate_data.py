import sys
import math

AR_dist_means = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]

AoA_means = [eval(x) for x in ['pi/6.', 'pi/5.', 'pi/4.', 'pi/3.', 'pi/2.']]

trials = range(1,6)


for ar_mean in AR_dist_means:
	for aoa_mean in AoA_means:
		aggregator = []
		for trial_num in trials:
			csv_name = 'AR_%f_AoA_%f_trial_%d.csv' % (ar_mean, aoa_mean, trial_num)
			fh = open(csv_name, 'r')
			csv_buf = fh.read()
			split_by_line = csv_buf.split('\n')
			if split_by_line[0] == 'cell_#,angle_of_attachment,aspect_ratio,number_of_cells,cumulative_overlap,cumulative_squared_overlap,max_overlap_of_single_cell,generation_#\n':
				
			split.by_value


sys.exit(0)