#!/bin/bash
#
# This script runs FreeSurfer 6.0 recon-all
# and makes a base for two timepoints, which includes the
# all morphological measurements at vertex
# and parcellated scales. Run this script
# by running the batch_base.sh file
# and calling on subject_list_base.txt
#

echo -e "\nSetting Up Freesurfer6.0"

source /projects/adapt_lab/shared/ADS/Scripts/sMRI/SetUpFreeSurfer.sh 

echo -e "\nFreesurfer Home is $FREESURFER_HOME"

echo -e "\nThe Subject Directory is $SUBJECTS_DIR"

echo -e "\Running recon-all on ${SUBID}"

recon-all -base "${SUBID}" -tp /projects/adapt_lab/shared/ADS/data/BIDS_data/derivatives/freesurfer/"${SUBID}"_ses-wave2 -tp /projects/adapt_lab/shared/ADS/data/BIDS_data/derivatives/freesurfer/"${SUBID}"_ses-wave3 -all
