#!/bin/bash
# This script calls on the rest_cohort.csv and batch submits for each participant in that file
# to the xcpEngine fc-ICA-AROMA preprocessing stream
# Specificially, it will make a .csv file that looks something like this: rest_cohort.csv.sub-SH166,ses-1,run-1.csv

# Set group and study variables

group_dir=/projects/adapt_lab/shared
study="SHARP"

# Point to the FULL cohort file that we'll be pulling from

FULL_COHORT=/projects/adapt_lab/shared/SHARP/SHARP_Scripts/rsfMRI/xcpEngine/rest_cohort.csv

# This creates an array so that it can be called in the for loop below. I'm sure there's a more elegant way to do this but this is what I got

readarray SUBJLIST < rest_cohort.csv

# Start the submission process

for SUBJ in $(seq 1 $(cat rest_cohort.csv | wc -l)); do

# This will create a temporary .csv file for each participant which can be called in the job script 

ID=${SUBJLIST[SUBJ]%%,/*} # This just gives us the ID of the participant (including wave)
HEADER=$(head -n 1 $FULL_COHORT) # This pulls the first row of the .csv file above (id0,id1,img)
LINE=$(awk "NR==$(expr $SUBJ + 1)" $FULL_COHORT ) # gets the row corresponding to our specific sub
TEMP_COHORT=${FULL_COHORT}.${ID}.csv # creates the csv file
echo $HEADER > $TEMP_COHORT # Writes the header row to the file
echo $LINE >> $TEMP_COHORT # Writes the subject specific row to the file

# This gets the session and the runs, becasue I couldn't figure out a way to pass a variable with a comma in it, so we'll just have to put them together in the job script

ses=${TEMP_COHORT#*,}
ses=${ses%%,*}
run=${TEMP_COHORT##*,}


sbatch --export ALL,ID=${ID},TEMP_COHORT=${TEMP_COHORT},ses=${ses},run=${run} --job-name xcp_rest_"${ID}" --partition=long --mem=40G -o "${group_dir}"/"${study}"/SHARP_Scripts/rsfMRI/xcpEngine/output/"${ID}"_xcp_rest_output.txt -e "${group_dir}"/"${study}"/SHARP_Scripts/rsfMRI/xcpEngine/output/"${ID}"_xcp_rest_error.txt xcp_rest.sh


done
