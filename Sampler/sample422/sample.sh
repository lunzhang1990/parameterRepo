#!/bin/bash 
# Active comments for SLURM
#SBATCH -n 1                  # One task
#SBATCH -c 1                 # One cpu per task
#SBATCH -N 1                   # Minimum one node
#SBATCH -t 3-00:00:00            # Runtime in D-HH:MM
#SBATCH -p mischaik_1 # Partition to submit to

#SBATCH --output=testslurm%N.%j.out    # Output file
#SBATCH --error=slurm_script.%N.%j.err     # Error output file
#SBATCH --mail-user=chamberlian1990@gmail.com  # User e-mail
#SBATCH --mail-type=FAIL         # When to send e-mail
#SBATCH --mem=8G # 16GB of memory


srun python samplerun.py 4_2_2  422prec3.dat
