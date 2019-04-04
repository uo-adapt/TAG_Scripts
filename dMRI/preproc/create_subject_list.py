# This script wil take a list made from the lcni directory
# and will strip the excess leaving all the names
import os

# Set study info (may need to change for your study)
# These variables are used only in this file for paths. Can omit if wanted.
group = "adapt_lab"
study = "SHARP"
PI = "Allen"
scriptsFolder = "SHARP_Scripts"

# The following variables are used in the main script and need to be defined here. 
# They need to exist prior to running the script

# Directories
parentdir = os.path.join(os.sep, "projects", group, "shared", study) # folder that contains bidsdir and codedir
bidsdir = os.path.join(parentdir,"bids_data")
codedir = os.path.join(parentdir, scriptsFolder, "dMRI", "preproc") # Contains subject_list.txt, config file, and dcm2bids_batch.py

# List the subject directory names, store them, then sort
subjectdir_contents = os.listdir(bidsdir)
subjectdir_contents.sort()

# Remove any directory names that don't contain SH in them (like 'derivatives')
subjectdir_contents = list(filter(lambda k: 'SH' in k, subjectdir_contents))

# list of subjects to be ommitted from 'subject_list.txt'
thing = ['sub-SH219',"sub-SH227","sub-SH231"]

# Remove list of subjects from the list
for i in thing:
	if i in str(subjectdir_contents):
	 subjectdir_contents.remove(i)

# Remove 'sub-' from the directory names, leaving only participant IDs
for subject in range(len(subjectdir_contents)):
	subjectdir_contents[subject] = subjectdir_contents[subject][4:]

# Write the subject list to a text file
with open(os.path.join(codedir,"subject_list.txt"), mode="w") as outfile:  # also, tried mode="rb"
    for subject in subjectdir_contents:
        outfile.write("%s\n" % subject)




