import sys
import math
import pandas as pd


def aggregate_frames(frames, filename):
	length_of_shortest_frame = min(frames, key=lambda frame: frame.shape[0]).shape[0]
	truncated_frames = map(lambda frame: frame[0:length_of_shortest_frame], frames)
	# this is absurdly simple and I love Python
	average_frame = sum(truncated_frames) / len(truncated_frames)
	fh = open(aggregate_name, 'w')
	avg_frame.to_csv(fh)
	fh.close()


def max_numcells(frames, thresholds):
	threshold_to_trials = {}
	num_records = frame.shape[0]
	for threshold in thresholds:
		trial = 1
		for frame in frames:
			trials_to_numcells = {}
			for i in range(num_records):
				num_cells = frame[i: i+1].number_of_cells
				cumulative_squared_overlap = frame[i: i+1].cumulative_squared_overlap
				if cumulative_squared_overlap >= threshold:
					# will record the number of cells 1 cell AFTER the threshold was reached
					trials_to_numcells[trial] = num_cells
					break
			trial += 1
		threshold_to_trials[threshold] = trials_to_numcells
	return threshold_to_trials


def aggregate_numcells_by_params(thresholds_to_trials, filename):
	fh = open(filename, 'w')
	df = pd.DataFrame(thresholds_to_trials)
	df.to_csv(fh)
	fh.close()


#TODO
def aggregate_numcells_at_threshold_by_params():
	pass

# 1.0, 1.1, 1.2, 1.3, 1.4,

AR_dist_means = [ 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]

AoA_means = [eval(x) for x in ['pi/6.', 'pi/5.', 'pi/4.', 'pi/3.', 'pi/2.']]

thresholds = [0.1*603504., 0.2*603504., 0.3*603504., 0.4*603504., 0.5*603504., 0.6*603504., 0.7*603504., 0.8*603504., 0.9*603504., 603504.]

trials = range(1,101)

for ar_mean in AR_dist_means:
	for aoa_mean in AoA_means:
		data_frames = []
		frame_to_threshold_dicts = {}
		for trial_num in trials:
			try:
				csv_name = 'AR_%f_AoA_%f_trial_%d.csv' % (ar_mean, aoa_mean, trial_num)
				df = pd.read_csv(csv_name)
				data_frames.append(df)
			except IOError:
				pass
		aggregate_name = 'AR_%f_AoA_%f_MEAN.csv' % (ar_mean, aoa_mean)
		aggregate_frames(data_frames, aggregate_name)
		thresholds_to_numcells_name = 'AR_%f_AoA_%f_NUMCELLS_at_OVERLAP.csv' % (ar_mean, aoa_mean)
		thresholds_to_numcells_by_trial = max_numcells(data_frames, thresholds)
		aggregate_numcells_by_params(thresholds_to_numcells_by_trial)


sys.exit(0)