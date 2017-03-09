import sys
import math
import pandas as pd


def aggregate_frames(frames):
	length_of_shortest_frame = min(frames, key=lambda frame: frame.shape[0]).shape[0]
	truncated_frames = map(lambda frame: frame[0:length_of_shortest_frame], frames)
	# this is absurdly simple and I love Python
	average_frame = sum(truncated_frames) / len(truncated_frames)
	return average_frame


def max_numcells(frame, thresholds):
	threshold_to_numcells = {}
	num_records = frame.shape[0]
	for threshold in thresholds:
		for i in range(num_records):
			num_cells = frame[i: i+1].number_of_cells
			cumulative_squared_overlap = frame[i: i+1].cumulative_squared_overlap
			if cumulative_squared_overlap 

AR_dist_means = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]

AoA_means = [eval(x) for x in ['pi/6.', 'pi/5.', 'pi/4.', 'pi/3.', 'pi/2.']]

trials = range(1,101)

for ar_mean in AR_dist_means:
	for aoa_mean in AoA_means:
		data_frames = []
		for trial_num in trials:
			csv_name = 'AR_%f_AoA_%f_trial_%d.csv' % (ar_mean, aoa_mean, trial_num)
			df = pd.read_csv(csv_name)
			data_frames.append(df)
		aggregate_name = 'AR_%f_AoA_%f_AGGREGATE.csv' % (ar_mean, aoa_mean)
		fh = open(aggregate_name, 'w')
		avg_frame = aggregate_frames(data_frames)
		avg_frame.to_csv(fh)

			


sys.exit(0)