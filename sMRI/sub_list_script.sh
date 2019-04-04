#!/bin/bash
# 
# This script makes a list of all of the freesurfer
# directories that have both session 2 and 3 output
# then puts them into a subject list for both the use
# of making the freesurfer base and the longitudinal ouptut
#params:
inputDir="/projects/adapt_lab/shared/ADS/data/BIDS_data/derivatives/freesurfer"
outputDir="/projects/adapt_lab/shared/ADS/Scripts/sMRI/"
outputFile="subject_list_base.txt"
# cd into /projects/adapt_lab/shared/ADS/data/BIDS_data/derivatives/freesurfer
cd $inputDir
declare -a newArray
readarray -t newArray < 
ls -d sub-* > subList.txt
declare -a fullArray
readarray -t fullArray < subList.txt
# echo ${fullArray[@]}
declare -a multSessArray
 
for i in `seq 0 $((${#fullArray[@]}-1))`
do
currentName=${fullArray[i]}
nextName=${fullArray[i+1]}
currentLength=${#currentName}
nextLength=${#nextName}
currentSub=${fullArray[i]:0:$(($currentLength-10))} 
nextSub=${fullArray[i+1]:0:$(($nextLength-10))} 
#if the current sub matches the next sub, include it + the next; otherwise don't.
if [ "$currentSub" =  "$nextSub" ]
then
# append current + next NAMES
echo $currentSub
multSessArray+=($currentSub)
 fi
 
 done
 printf "%s\n" "${multSessArray[@]}" > multSessArray.txt
mv multSessArray.txt $outputDir/$outputFile
cd $outputDir
