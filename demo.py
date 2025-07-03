#!/usr/bin/env python3
"""
Demo script for CSV Similarity Parser
Shows how the tool works with a simple example
"""

import pandas as pd
from datetime import datetime

def create_demo_csvs():
    """Create demo CSV files to show how the tool works"""
    
    # Create CSV 1 (Reference file)
    csv1_data = {
        'Username': ['john.doe@company.com', 'jane.smith@company.com', 'bob.wilson@company.com'],
        'First Name': ['John', 'Jane', 'Bob'],
        'Last Name': ['Doe', 'Smith', 'Wilson'],
        'Department': ['IT', 'HR', 'Sales'],
        'Role': ['Developer', 'Manager', 'Representative']
    }
    
    csv1_df = pd.DataFrame(csv1_data)
    csv1_df.to_csv('demo_csv1.csv', index=False)
    
    # Create CSV 2 (File to process)
    csv2_data = {
        'Username': ['john.doe@company.com', 'jane.smith@company.com', 'alice.jones@company.com', 'bob.wilson@company.com'],
        'First Name': ['John', 'Jane', 'Alice', 'Bob'],
        'Last Name': ['Doe', 'Smith', 'Jones', 'Wilson'],
        'Department': ['IT', 'HR', 'Marketing', 'Sales'],
        'Manager': ['Manager A', 'Manager B', 'Manager C', 'Manager D'],
        'Project': ['Project Alpha', 'Project Beta', 'Project Gamma', 'Project Delta']
    }
    
    csv2_df = pd.DataFrame(csv2_data)
    csv2_df.to_csv('demo_csv2.csv', index=False)
    
    print("✓ Created demo CSV files:")
    print("  - demo_csv1.csv (Reference file)")
    print("  - demo_csv2.csv (File to process)")
    print()

def run_demo():
    """Run the demo processing"""
    
    print("=== CSV Similarity Parser Demo ===")
    print()
    
    # Create demo files
    create_demo_csvs()
    
    # Load the files
    csv1_data = pd.read_csv('demo_csv1.csv')
    csv2_data = pd.read_csv('demo_csv2.csv')
    
    print("CSV 1 (Reference File):")
    print(csv1_data.to_string(index=False))
    print()
    
    print("CSV 2 (File to Process):")
    print(csv2_data.to_string(index=False))
    print()
    
    # Define mappings (what the GUI would do)
    column_mappings = {
        'Username': 'Username',
        'First Name': 'First Name',
        'Last Name': 'Last Name',
        'Department': 'Department'
    }
    
    # Define matching columns
    matching_columns = {'Username', 'First Name', 'Last Name', 'Department'}
    
    print("Column Mappings:")
    for csv1_col, csv2_col in column_mappings.items():
        print(f"  {csv1_col} → {csv2_col}")
    print()
    
    print("Matching Columns:")
    for col in matching_columns:
        print(f"  ✓ {col}")
    print()
    
    # Process the files
    output_data = csv2_data.copy()
    approval_column = "Approval Status"
    output_data[approval_column] = "NO"
    
    # Create lookup set from CSV 1
    csv1_lookup = set()
    for _, row in csv1_data.iterrows():
        match_values = []
        for csv1_header in matching_columns:
            csv2_header = column_mappings[csv1_header]
            value = str(row[csv1_header]).strip()
            match_values.append(value)
        csv1_lookup.add(tuple(match_values))
    
    # Process CSV 2 rows
    matches_found = 0
    for idx, row in output_data.iterrows():
        match_values = []
        for csv1_header in matching_columns:
            csv2_header = column_mappings[csv1_header]
            value = str(row[csv2_header]).strip()
            match_values.append(value)
        
        if tuple(match_values) in csv1_lookup:
            output_data.at[idx, approval_column] = "YES"
            matches_found += 1
    
    # Save output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"demo_output_{timestamp}.csv"
    output_data.to_csv(output_filename, index=False)
    
    print("Processing Results:")
    print(f"  Total rows in CSV 2: {len(csv2_data)}")
    print(f"  Matches found: {matches_found}")
    print(f"  Output file: {output_filename}")
    print()
    
    print("Output CSV (with approval status):")
    print(output_data.to_string(index=False))
    print()
    
    print("=== Demo Complete ===")
    print()
    print("To run the full GUI application:")
    print("  python csv_similarity_parser.py")
    print()
    print("To test with your own files:")
    print("  1. Replace demo_csv1.csv and demo_csv2.csv with your files")
    print("  2. Run the GUI application")
    print("  3. Follow the on-screen instructions")

if __name__ == "__main__":
    run_demo() 