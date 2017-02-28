import sys
from math import pi


AR_dist_means = [2.0] #[1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]

AoA_means = ['pi/6.', 'pi/5.', 'pi/4.', 'pi/3.', 'pi/2.']

AoA_means = map(lambda x: eval(x), AoA_means)

trial_nums = range(1,6)

for AR_mean in AR_dist_means:
	for AoA_mean in AoA_means:
		for trial_num in trial_nums:

			filename = 'fitness_data/AR_%f_AoA_%f_trial_%d.csv' % (AR_mean, AoA_mean, trial_num)
			if filename != 'AR_1.100000_AoA_0.523599_trial_1.csv':
				fh = open(filename, 'r+')

				dat_buf = fh.read()
				dat_buf = dat_buf.split('\n')
				fh.seek(0)
				fh.truncate()

				new_header = ''.join(dat_buf[0:3])
				old_data = '\n'.join(dat_buf[3:len(dat_buf) - 1]) + dat_buf[len(dat_buf) - 1]
				new_filecontents = '\n'.join([new_header, old_data])

				fh.write(new_filecontents)
				fh.close()
sys.exit(0)