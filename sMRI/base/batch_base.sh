#!/bin/bash
#
# This batch file calls on your subject
# list (named subject_list_base.txt). And 
# runs the job_base.sh file for 
# each subject. It saves the ouput
# and error files in their specified
# directories.
#
# Set your study
STUDY=/projects/adapt_lab/shared/ADS

# Set subject list
SUBJLIST=`cat subject_list_base.txt`
#SUBJLIST=`cat test.txt`

# 
for SUBJ in $SUBJLIST
do
 sbatch --export SUBID=${SUBJ} --job-name base_reconall_"${SUBJ}" --partition=short --mem-per-cpu=4G --time=24:00:00 --cpus-per-task=1 -o "${STUDY}"/Scripts/sMRI/base/output/"${SUBJ}"_base_reconall_output.txt -e "${STUDY}"/Scripts/sMRI/base/output/"${SUBJ}"_base_reconall_error.txt job_base.sh
done
