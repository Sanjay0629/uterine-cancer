#!/bin/bash
echo "Starting TCGA Uterine Cancer ML API..."
echo "==================================================="

cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install requirements
echo "Installing/Checking dependencies..."
pip install -r requirements.txt

# Run Application
echo ""
echo "Starting Flask Server on port 5000..."
python3 api/app.py
