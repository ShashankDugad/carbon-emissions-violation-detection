# NYU Greene HPC Setup Guide

## Team Members
- **Shashank Dugad** (sd5957) - Data Pipeline & ML
- **Anshi Shah** (ans10020) - Batch Processing & Analytics
- **Ronit Gehani** (rg4881) - Streaming & Production

## First Time Setup (All Team Members)

### 1. SSH to Greene
```bash
ssh YOUR_NETID@greene.hpc.nyu.edu
```

### 2. Generate SSH Key for GitHub
```bash
ssh-keygen -t ed25519 -C "YOUR_NETID@nyu.edu" -f ~/.ssh/id_ed25519_greene
# Press Enter 3 times (no passphrase)

# Display public key
cat ~/.ssh/id_ed25519_greene.pub
```

**Add this key to GitHub:**
- Go to https://github.com/settings/keys
- Click "New SSH key"
- Title: "NYU Greene HPC - YOUR_NAME"
- Paste the key

### 3. Configure SSH for GitHub
```bash
cat >> ~/.ssh/config << 'SSHEOF'
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_greene
SSHEOF

chmod 600 ~/.ssh/config

# Test connection
ssh -T git@github.com
```

### 4. Clone Repository
```bash
cd ~
git clone git@github.com:ShashankDugad/carbon-emissions-violation-detection.git carbon-emissions-project
cd carbon-emissions-project
```

### 5. Run Setup Script
```bash
bash setup_greene_env.sh
```

### 6. Configure Environment (Add to ~/.bashrc)
```bash
cat >> ~/.bashrc << 'ENVEOF'
# Carbon Emissions Detection Project
module load python/intel/3.8.6
export JAVA_HOME=/share/apps/jdk/1.8.0_271
export PATH=$JAVA_HOME/bin:$HOME/.local/bin:$PATH
export PROJECT_HOME=$HOME/carbon-emissions-project
ENVEOF

source ~/.bashrc
```

## Verify Setup
```bash
# Check environment
module list
python3 --version  # Should be 3.8.6
java -version      # Should be 1.8.0_402
pyspark --version  # Should be 3.5.1

# Check project
cd $PROJECT_HOME
pwd
ls -la
```

## Storage & Quotas

- **Home Directory:** `/home/YOUR_NETID`
- **Quota:** 2TB
- **Check usage:** `quota -s`

## Running PySpark

### Interactive Shell
```bash
pyspark --master local[4] --driver-memory 4g
```

### Submit Spark Job (Slurm)
```bash
sbatch scripts/slurm_templates/spark_job.slurm
```

## Slurm Partitions

- `cs` - CPU compute nodes (default)
- `short` - Quick jobs (<4 hours)
- `gpu` - GPU nodes (if needed)

Check available resources:
```bash
sinfo
squeue -u $USER
```

## Troubleshooting

### "JAVA_HOME is not set"
```bash
export JAVA_HOME=/share/apps/jdk/1.8.0_271
export PATH=$JAVA_HOME/bin:$PATH
```

### "pyspark: command not found"
```bash
export PATH=$HOME/.local/bin:$PATH
```

### Permission denied (GitHub)
```bash
ssh -T git@github.com  # Should say "Hi YOUR_USERNAME!"
```

## Useful Commands
```bash
# Check job status
squeue -u $USER

# Check storage
quota -s

# Pull latest changes
cd $PROJECT_HOME
git pull origin main

# View logs
tail -f logs/spark_job.log
```

## Resources

- Greene Documentation: https://sites.google.com/nyu.edu/nyu-hpc/hpc-systems/greene
- Slurm Tutorial: https://sites.google.com/nyu.edu/nyu-hpc/training-support/tutorials/slurm-tutorial
- Project GitHub: https://github.com/ShashankDugad/carbon-emissions-violation-detection
