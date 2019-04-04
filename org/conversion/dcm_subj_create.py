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
dicomdir = os.path.join(os.sep, "projects", "lcni", "dcm", group, "Archive", "sharp")
parentdir = os.path.join(os.sep, "projects", group, "shared", study) # folder that contains bidsdir and codedir
codedir = os.path.join(parentdir, scriptsFolder, "org", "conversion") # Contains subject_list.txt, config file, and dcm2bids_batch.py

subjectdir_contents = os.listdir(dicomdir)
subjectdir_contents.sort()

# filter subject directory for anything less than 16 characters (this is study specific)
subjectdir_contents = filter(lambda k: len(k) < 16, subjectdir_contents)

# filters subject directory for anything with 'SH' in the name (this is study specific)
subjectdir_contents = list(filter(lambda k: 'SH' in k, subjectdir_contents))

# duplicates each line separated by "," (e.g., "SH149" becomes "SH149,SH149")
subjectdir_contents = [subject + "," + subject for subject in subjectdir_contents]

# Removes the last 9 characters of each line 
for subject in range(len(subjectdir_contents)):
	subjectdir_contents[subject] = subjectdir_contents[subject][:-9]

# adds a ",1" to the end of each line (to indicate session)
subjectdir_contents = [subject + ",1" for subject in subjectdir_contents]

with open(os.path.join(codedir,"subject_list.txt"), mode="w") as outfile:  # also, tried mode="rb"
    for subject in subjectdir_contents:
        outfile.write("%s\n" % subject)




