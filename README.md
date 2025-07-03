# CSV Similarity Parser

A Python tool that compares two CSV files and creates a third CSV file with approval status based on exact row matches.

## Features

- **Header Mapping**: Automatically suggests column mappings between CSV files with user override capability
- **Flexible Matching**: User can select which columns to use for exact matching
- **GUI Interface**: Simple and intuitive graphical user interface
- **Auto-naming**: Automatically generates output filename
- **Error Handling**: Robust handling of missing data and different column structures
- **Cross-platform**: Works on Windows, macOS, and Linux

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Setup

#### Option 1: Automated Installation (Recommended)

**On macOS/Linux:**
```bash
chmod +x install.sh run.sh
./install.sh
```

**On Windows:**
```cmd
install.bat
```

#### Option 2: Manual Setup

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

#### Option 1: Quick Start
```bash
# On macOS/Linux:
./run.sh

# On Windows:
run.bat
```

#### Option 2: Manual Start
```bash
# Activate virtual environment first
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Run the application
python csv_similarity_parser.py
```

### Using the GUI

1. **File Selection**:
   - Click "Browse" to select your first CSV file (reference file)
   - Click "Browse" to select your second CSV file (file to be processed)

2. **Column Mapping**:
   - Review the automatically suggested column mappings
   - Use "Edit Mapping" to modify any mappings
   - Use "Remove Mapping" to remove unwanted mappings
   - Use "Auto Map" to regenerate suggestions

3. **Matching Configuration**:
   - Select which columns to use for exact matching (checkboxes)
   - All mapped columns are selected by default

4. **Approval Column**:
   - Enter a name for the new approval column (default: "Approval Status")

5. **Processing**:
   - Click "Process Files" to generate the output CSV
   - Monitor progress in the status log

### Output

- The tool creates a new CSV file with all rows from the second file
- Adds a new column with "YES" for rows that have exact matches in the first file
- Adds "NO" for rows that don't have matches
- Output filename format: `{original_name}_with_approval_{timestamp}.csv`

## Example

**CSV 1 (Reference)**:
```
Username,First Name,Last Name,Group
brian.dawson@numo.com,Brian,Dawson,admin
john.doe@company.com,John,Doe,user
```

**CSV 2 (To Process)**:
```
Username,First Name,Last Name,Group,Manager
brian.dawson@numo.com,Brian,Dawson,admin,Manager A
jane.smith@company.com,Jane,Smith,user,Manager B
```

**Output CSV**:
```
Username,First Name,Last Name,Group,Manager,Approval Status
brian.dawson@numo.com,Brian,Dawson,admin,Manager A,YES
jane.smith@company.com,Jane,Smith,user,Manager B,NO
```

## Testing

The project includes sample CSV files and a test script to verify functionality:

```bash
# Run the test script
python test_functionality.py
```

**Test Results** (with sample data):
- ✓ Loaded CSV 1: 8 rows, 6 columns
- ✓ Loaded CSV 2: 10 rows, 8 columns
- ✓ Processing complete: 10 rows processed, 2 matches found
- ✓ Expected matches verified: All test cases passed

## Performance

- **Recommended maximum**: 100,000 rows per CSV file
- **Processing time**: Depends on file size and number of columns used for matching
- **Memory usage**: Scales linearly with file size
- **Optimization**: Uses efficient lookup sets for fast matching

## Project Structure

```
csvSimilarityParser/
├── csv_similarity_parser.py    # Main application
├── requirements.txt            # Python dependencies
├── setup.py                   # Package setup script
├── install.sh                 # Unix installation script
├── install.bat                # Windows installation script
├── run.sh                     # Unix quick start script
├── run.bat                    # Windows quick start script
├── test_functionality.py      # Test script
├── sample_csv1.csv            # Sample reference CSV
├── sample_csv2.csv            # Sample CSV to process
├── README.md                  # This file
└── venv/                      # Virtual environment (created during installation)
```

## Troubleshooting

- **"No module named 'pandas'"**: Run `pip install -r requirements.txt`
- **GUI not appearing**: Ensure you're running on a system with GUI support
- **Large files slow**: Consider splitting very large files or using fewer columns for matching
- **Permission denied on scripts**: Run `chmod +x install.sh run.sh` (Unix/macOS)

## Deployment

The tool is designed for easy deployment:

1. **Copy the entire project folder** to the target machine
2. **Run the appropriate installation script**:
   - `install.sh` for Unix/macOS
   - `install.bat` for Windows
3. **Use the quick start scripts** to run the application

No additional system dependencies are required beyond Python 3.8+.

## License

This project is open source and available under the MIT License. 