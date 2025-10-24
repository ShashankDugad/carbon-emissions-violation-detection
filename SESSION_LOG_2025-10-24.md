# Greene HPC Setup Session - October 24, 2025

## Completed by: Shashank Dugad (sd5957)

## Accomplishments

### 1. Greene Environment Setup ✓
- Connected to Greene HPC: `log-3.hpc.nyu.edu`
- Python 3.8.6 loaded
- PySpark 3.5.1 installed (user space)
- Java 1.8.0_402 configured
- 2TB storage quota available

### 2. GitHub Integration ✓
- SSH key generated and added to GitHub
- Repository cloned: `~/carbon-emissions-project`
- Team documentation created: `GREENE_SETUP.md`
- Setup script created: `setup_greene_env.sh`

### 3. Data Download Tested ✓
- AWS CLI configured (no-sign-request for public bucket)
- OpenAQ download successful from S3: `s3://openaq-data-archive`
- Test data: Location 2178, year 2023, 331 files, 173KB compressed
- Schema validated: 9 columns confirmed

### 4. Environment Configuration
```bash
# Added to ~/.bashrc
module load python/intel/3.8.6
export JAVA_HOME=/share/apps/jdk/1.8.0_271
export PATH=$JAVA_HOME/bin:$HOME/.local/bin:$PATH
export PROJECT_HOME=$HOME/carbon-emissions-project
```

### 5. Installed Packages
- pyspark==3.5.1
- pandas
- numpy
- boto3
- s3fs
- awscli

## Data Validation Results

**Sample Data (Location 2178, 2023):**
- Files: 331 CSV.GZ files
- Size: 173KB compressed
- Schema: location_id, sensors_id, location, datetime, lat, lon, parameter, units, value
- Parameters detected: NO2 (likely others)
- Data quality: Clean, no missing values in sample

## Storage Estimates

Based on 1 location × 1 year = 173KB:
- 1,178 locations × 5 years = **1,178 × 5 × 173KB ≈ 1.0 GB compressed**
- Matches our Colab estimate of **2.1 GB Parquet** after decompression

## Next Steps

### For Team Members (Anshi, Ronit)
1. Follow `GREENE_SETUP.md` to set up your environment
2. Run `bash setup_greene_env.sh` after cloning repo
3. Test download: `bash scripts/download/test_download.sh`

### For Shashank (Next Session)
1. Create full download script for 1,178 locations
2. Convert CSV.GZ → Parquet with PySpark
3. Implement partitioning strategy (location_id, year)
4. Create data quality validation pipeline
5. Set up Slurm job for batch processing

## Files Created
- `GREENE_SETUP.md` - Team setup guide
- `setup_greene_env.sh` - Automated setup script
- `scripts/download/download_openaq_sample.sh` - Sample download
- `scripts/download/validate_openaq_sample.py` - Data validation
- `scripts/download/test_download.sh` - Test script (used)

## Resources
- Greene Docs: https://sites.google.com/nyu.edu/nyu-hpc/hpc-systems/greene
- OpenAQ Docs: https://docs.openaq.org
- Project Repo: https://github.com/ShashankDugad/carbon-emissions-violation-detection

---
**Session Duration:** ~2 hours  
**Status:** ✓ Environment ready for data ingestion phase
