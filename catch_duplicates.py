import sys
import os


seen_files = []

filenames = os.listdir(os.getcwd())

for filename in filenames:
    if filename in seen_files:
        print filename
    else:
        seen_files.append(filename)


sys.exit(0)