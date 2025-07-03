#!/bin/bash

# CSV Similarity Parser Installation Script
# This script sets up the CSV Similarity Parser tool on Unix-based systems

echo "=== CSV Similarity Parser Installation ==="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.8 or higher is required. Current version: $python_version"
    exit 1
fi

echo "✓ Python $python_version detected"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed. Please install pip3."
    exit 1
fi

echo "✓ pip3 detected"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "=== Installation Complete ==="
echo ""
echo "To run the CSV Similarity Parser:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the application: python csv_similarity_parser.py"
echo ""
echo "Or use the quick start script: ./run.sh"
echo ""

# Make run script executable
chmod +x run.sh

echo "Installation completed successfully!" 