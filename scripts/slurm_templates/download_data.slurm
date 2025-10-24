#!/bin/bash
#SBATCH --job-name=openaq_download
#SBATCH --output=logs/download_%j.out
#SBATCH --error=logs/download_%j.err
#SBATCH --time=04:00:00
#SBATCH --mem=4GB
#SBATCH --cpus-per-task=2
#SBATCH --partition=cs

# Load environment
module load python/intel/3.8.6
export PATH=$HOME/.local/bin:$PATH

# Navigate to project
cd $HOME/carbon-emissions-project

# Run download
echo "Starting OpenAQ download at $(date)"
bash scripts/download/download_openaq_full.sh
echo "Completed at $(date)"
