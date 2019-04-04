#!/bin/bash
#
# This batch file calls on your subject
# list (named subject_list_base.txt). And 
# runs the job_long_T3.sh file for 
# each subject. It saves the ouput
# and error files in their specified
# directories.
#
# Set your study
STUDY=/projects/adapt_lab/shared/ADS

# Set subject list
SUBJLIST=`cat subject_list_long.txt`
#SUBJLIST=`cat test.txt`

# 
for SUBJ in $SUBJLIST
do
 sbatch --export SUBID=${SUBJ} --job-name long_reconall_"${SUBJ}" --partition=short --mem-per-cpu=4G --time=20:00:00 --cpus-per-task=1 -o "${STUDY}"/Scripts/sMRI/longitudinal/output/"${SUBJ}"_long_T3_reconall_output.txt -e "${STUDY}"/Scripts/sMRI/longitudinal/output/"${SUBJ}"_long_T3_reconall_error.txt job_long_T3.sh
done

