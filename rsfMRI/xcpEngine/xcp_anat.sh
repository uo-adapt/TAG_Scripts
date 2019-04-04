#!/bin/bash
#

module load singularity
module load afni
module load ants
module load fsl
module load c3d
module load R
module load python3

cd /projects/adapt_lab/shared/SHARP/SHARP_Scripts/rsfMRI/xcpEngine

XCPEDIR=/projects/adapt_lab/shared/SHARP/SHARP_Scripts/rsfMRI/xcpEngine
SIMG=/projects/adapt_lab/shared/containers/xcpEngine.simg
HOME=/projects/adapt_lab/shared/SHARP

singularity run -B ${DATA_ROOT}:${HOME} $SIMG \
   -d ${HOME}/SHARP_Scripts/rsfMRI/xcpEngine/anat-Complete+_201901151515.dsn \
   -c "${TEMP_COHORT}",${ses} \
   -o ${HOME}/bids_data/derivatives/xcpEngine/data \
   -t 1 \
   -i \$TMPDIR

rm "${TEMP_COHORT}",${ses}