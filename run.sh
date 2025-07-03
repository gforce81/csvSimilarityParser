#!/bin/bash

# CSV Similarity Parser Quick Start Script

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running installation..."
    ./install.sh
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Run the application
echo "Starting CSV Similarity Parser..."
python csv_similarity_parser.py 