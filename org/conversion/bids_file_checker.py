# This file will check the structure of the bids directory and make sure that there 
# are the exact files necessary. If there are additional or missing files, this
# will return an error. 

import os
import json
from pprint import pprint
import pathlib
import subprocess
import numpy as np
from datetime import datetime
import pandas as pd

# Set study info (may need to change for your study)
# These variables are used only in this file for paths. Can omit if wanted.
Group="adapt_lab"
Study="SHARP"

# Change these to your own paths/times/etc.
parentdir = os.path.join(os.sep, "projects", Group, "shared", Study) # folder that contains bidsdir and codedir
bidsdir = os.path.join(parentdir, "bids_data") # where the niftis will be put
codedir = os.path.join(parentdir, "SHARP_Scripts", "org", "conversion") # Contains subject_list.txt, config file, and dcm2bids_batch.py
logdir = os.path.join(codedir, "logs_checker")
subject_list = os.path.join(codedir,"subject_list.txt")

try:
	# Create target Directory
	os.mkdir(logdir)
	print("Directory " , logdir ,  " Created ") 
except FileExistsError:
	print("Directory " , logdir ,  " already exists")

# Change these to match teh types of files you have for your study (e.g., remove fmap if you don't have field maps)
scan_type_list = {"anat","func","dwi"}


# Copy and paste the tail of each file (i.e., everything after `sub-xxx_ses-wavex_`) into their respective variable 
d = {'anat': ["run-01_T1w.json","run-01_T1w.nii.gz","run-02_T1w.json","run-02_T1w.nii.gz"], \
	'func': ["task-rest_run-01_bold.json","task-rest_run-01_bold.nii.gz","task-rest_run-02_bold.json","task-rest_run-02_bold.nii.gz"], \
	'dwi': ["acq-lr_dwi.bval","acq-lr_dwi.bvec","acq-lr_dwi.json","acq-lr_dwi.nii.gz","acq-rl_dwi.bval","acq-rl_dwi.bvec","acq-rl_dwi.json","acq-rl_dwi.nii.gz"]}

# turns the dictionary above (`d`) into a dataframe
scan_list = pd.DataFrame.from_dict(d, orient='index')
scan_list = scan_list.transpose()

# Each wave that should be represented. It should be noted that this script assumes the same number and type of 
# scans are the same throughout each run. If this is not the case...good luck coding!
waves = {"1"}


def write_to_errorlog(message,error_type):
	"""
	Write a log message to the error log, specific to the type of error. Also print it to the terminal.

	@type message:          string
	@param message:         Message to be printed to the log
	"""
	errorlog = os.path.join(logdir, error_type + "_errorlog_dcmchecker" + datetime.now().strftime("%Y%m%d-%H%M") +  ".txt")
	with open(errorlog, 'a') as logfile:
		logfile.write(message + os.linesep)
	print(message)

# Without further ado, here's the function!

with open(subject_list) as file: 
	lines = file.readlines()
	subjects = []
	for line in lines:
		entry = line.strip()
		subjects.append(entry.split(",")[1]) # Keep only subject name from the `subject_list.txt`
	subjects = list(set(subjects)) # Removes duplicate subject names (don't worry, it'll still for check all waves)
	for subject in subjects:
		subjectpath = os.path.join(bidsdir,"sub-"+subject)
		if os.path.isdir(subjectpath):
			for wave in waves:
				if os.path.isdir(os.path.join(subjectpath,"ses-" + wave)): # Checking to make sure that the participant has each wave
					scan_types = os.listdir(os.path.join(subjectpath,"ses-" + wave))
					if ".DS_Store" in scan_types: # Remove pesky hidden files
						scan_types.remove(".DS_Store")
					scan_type_missing = list(set(scan_type_list)-set(scan_types)) # create a list of missing scan types within a wave (e.g., "func", "anat")
					for scan_type_missing in scan_type_missing:
						write_to_errorlog(scan_type_missing + " is missing for " + subject + ", ses" + wave + os.linesep, error_type = scan_type_missing) # Write to error log the missing scan types
					for scan_type in scan_types:
						scans = os.listdir(os.path.join(subjectpath,"ses-" + wave, scan_type))
						if ".DS_Store" in scans:
								scans.remove(".DS_Store")
						check_scans = ["sub-" + subject + "_ses-" + wave + "_" + file for file in scan_list[scan_type] if type(file) == str]
						missing_list = list(set(check_scans)-set(scans)) # Create a list of missing scans within scan types
						for missing in missing_list:
								write_to_errorlog(missing + " is missing for sub-" + subject + ", ses-" + wave + os.linesep, error_type = scan_type)
						extra_list = list(set(scans)-set(check_scans)) # If there are any extra scans or files that shouldn't be there, this will produce an error for it and write it to the log
						for extra in extra_list:
							write_to_errorlog(extra + " is an unrecognized file in sub-" + subject + ", ses-" + wave + os.linesep, error_type = scan_type)
						del [check_scans,missing_list,extra_list] # Cleaning up the workspace
					del [scan_types,scan_type_missing] # A little more cleaning
				else:
					write_to_errorlog(subject + " " + wave + " directory does not exist" + os.linesep, error_type = "wave") # Write to log if wave does not exist
		else:
			write_to_errorlog(subject + " directory does not exist" + os.linesep, error_type = "directory") # Write to log if participant does not exist 
		
