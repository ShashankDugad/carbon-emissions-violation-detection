#!/bin/bash
# Setup script for Carbon Emissions Detection Project on NYU Greene
# Team members: Run this once after cloning the repo

echo "=== Carbon Emissions Project - Greene Setup ==="

# 1. Load modules
module load python/intel/3.8.6

# 2. Set environment variables
export JAVA_HOME=/share/apps/jdk/1.8.0_271
export PATH=$JAVA_HOME/bin:$HOME/.local/bin:$PATH
export PROJECT_HOME=$HOME/carbon-emissions-project

# 3. Install Python dependencies
echo "Installing Python packages..."
pip3 install --user pyspark==3.5.1 pandas numpy boto3 s3fs pyyaml python-dotenv

# 4. Verify installations
echo ""
echo "=== Verification ==="
python3 --version
java -version 2>&1 | head -1
pip3 list | grep pyspark

echo ""
echo "✓ Setup complete!"
echo ""
echo "Add to your ~/.bashrc:"
echo "  module load python/intel/3.8.6"
echo "  export JAVA_HOME=/share/apps/jdk/1.8.0_271"
echo "  export PATH=\$JAVA_HOME/bin:\$HOME/.local/bin:\$PATH"
echo "  export PROJECT_HOME=\$HOME/carbon-emissions-project"
