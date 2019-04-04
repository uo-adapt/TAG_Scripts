# This script wil take a list made from the lcni directory
# and will strip the excess leaving all the names
import os
import csv

# Set study info (may need to change for your study)
# These variables are used only in this file for paths. Can omit if wanted.
group = "adapt_lab"
study = "SHARP"
PI = "Allen"
scriptsFolder = "SHARP_Scripts"

# The following variables are used in the main script and need to be defined here. 
# They need to exist prior to running the script

# Directories
parentdir = os.path.join(os.sep, "projects", group, "shared", study) 
codedir = os.path.join(parentdir, scriptsFolder, "rsfMRI", "xcpEngine") 
fmriprepdir = os.path.join(parentdir,"bids_data","derivatives","fmriprep")


# Each wave that should be represented. It should be noted that this script assumes the same number and type of 
# scans are the same throughout each run. If this is not the case...good luck coding!
waves = {"ses-1"}


# Change this to either be anatomical (anat) or functional (func)
preproc= "anat"

subjectdir_contents = os.listdir(fmriprepdir)

subjectdir_contents = list(filter(lambda k: 'sub-' in k, subjectdir_contents))
subjectdir_contents = [x for x in subjectdir_contents if not '.html' in x]
subjectdir_contents.sort()

with open(os.path.join(codedir, preproc + '_cohort.csv'),'w',newline='') as f1:
	writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
	head = ["id0,id1,img"]
	writer.writerow(head)
	for subject, wave in [(subject,wave) for subject in subjectdir_contents for wave in waves]:
		subjectpath = os.path.join(fmriprepdir,subject)
		if os.path.isdir(subjectpath):
			filepath = os.path.join(subjectpath,preproc,subject + "_desc-preproc_T1w.nii.gz")
			if os.path.isfile(filepath):
				row = [subject + "," + wave + "," + filepath]
				writer.writerow(row)
				