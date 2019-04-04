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
xcpdir = os.path.join(parentdir,"bids_data","derivatives","xcpEngine","data")

# Each wave that should be represented. It should be noted that this script assumes the same number and type of 
# scans are the same throughout each run. If this is not the case...good luck coding!
waves = {"ses-1"}
runs = {"run-01","run-02"}
tasks = {"rest"}



# Change this to either be anatomical (anat) or functional (rest)
preproc= "func"

subjectdir_contents = os.listdir(xcpdir)

subjectdir_contents = list(filter(lambda k: 'sub-' in k, subjectdir_contents))
subjectdir_contents = [x for x in subjectdir_contents if not '.html' in x]
subjectdir_contents.sort()

for task in tasks:
    with open(os.path.join(codedir, task + '_cohort.csv'),'w') as f1:
        writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
        head = ["id0,id1,id2,img,antsct"]
        writer.writerow(head)
        for subject, wave, run in [(subject,wave,run) for subject in subjectdir_contents for wave in waves for run in runs]:
            subjectpath = os.path.join(fmriprepdir,subject)
            if os.path.isdir(subjectpath):
                wavepath = os.path.join(subjectpath,wave)
                if os.path.isdir(wavepath):
                    filepath = os.path.join(wavepath,preproc,subject + "_" + wave + "_task-" + task + "_"+ run + "_space-T1w_desc-preproc_bold.nii.gz")
                    if os.path.isfile(filepath):
                        row = [subject + "," + wave + "," + run + "," + filepath + "," + os.path.join(xcpdir,subject,wave,"struc")]
                        writer.writerow(row)
                        