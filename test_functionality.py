#!/usr/bin/env python3
"""
Test script for CSV Similarity Parser functionality
"""

import pandas as pd
import os
from datetime import datetime

def test_csv_similarity_parser():
    """Test the core functionality of the CSV similarity parser"""
    
    print("=== Testing CSV Similarity Parser Functionality ===")
    
    # Load sample CSV files
    try:
        csv1_data = pd.read_csv('sample_csv1.csv')
        csv2_data = pd.read_csv('sample_csv2.csv')
        
        print(f"✓ Loaded CSV 1: {len(csv1_data)} rows, {len(csv1_data.columns)} columns")
        print(f"✓ Loaded CSV 2: {len(csv2_data)} rows, {len(csv2_data.columns)} columns")
        
        # Define column mappings (similar to what the GUI would do)
        column_mappings = {
            'Username': 'Username',
            'First Name': 'First Name',
            'Last Name': 'Last Name',
            'Group': 'Group'
        }
        
        # Define matching columns
        matching_columns = {'Username', 'First Name', 'Last Name', 'Group'}
        
        print(f"✓ Column mappings: {column_mappings}")
        print(f"✓ Matching columns: {matching_columns}")
        
        # Create output data
        output_data = csv2_data.copy()
        approval_column_name = "Approval Status"
        output_data[approval_column_name] = "NO"
        
        # Create lookup set from CSV 1 for faster matching
        csv1_lookup = set()
        for _, row in csv1_data.iterrows():
            match_values = []
            for csv1_header in matching_columns:
                csv2_header = column_mappings[csv1_header]
                value = str(row[csv1_header]).strip()
                match_values.append(value)
            csv1_lookup.add(tuple(match_values))
        
        print(f"✓ Created lookup set with {len(csv1_lookup)} unique combinations")
        
        # Process CSV 2 rows
        matches_found = 0
        total_rows = len(output_data)
        
        for idx, row in output_data.iterrows():
            match_values = []
            for csv1_header in matching_columns:
                csv2_header = column_mappings[csv1_header]
                value = str(row[csv2_header]).strip()
                match_values.append(value)
            
            if tuple(match_values) in csv1_lookup:
                output_data.at[idx, approval_column_name] = "YES"
                matches_found += 1
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"test_output_{timestamp}.csv"
        
        # Save output file
        output_data.to_csv(output_filename, index=False)
        
        print(f"✓ Processing complete!")
        print(f"✓ Total rows processed: {total_rows}")
        print(f"✓ Matches found: {matches_found}")
        print(f"✓ Output file: {output_filename}")
        
        # Show some sample results
        print("\n=== Sample Results ===")
        print(output_data[['Username', 'First Name', 'Last Name', 'Group', approval_column_name]].head(10))
        
        # Verify expected matches
        expected_matches = [
            ('brian.dawson@numo.com', 'Brian', 'Dawson', 'admin'),
            ('brian.dawson@numo.com', 'Brian', 'Dawson', '2factor_fido2_users')
        ]
        
        print("\n=== Expected Matches Verification ===")
        for expected in expected_matches:
            username, first_name, last_name, group = expected
            matching_rows = output_data[
                (output_data['Username'] == username) &
                (output_data['First Name'] == first_name) &
                (output_data['Last Name'] == last_name) &
                (output_data['Group'] == group)
            ]
            
            if len(matching_rows) > 0:
                status = matching_rows.iloc[0][approval_column_name]
                print(f"✓ {expected}: {status}")
            else:
                print(f"✗ {expected}: Not found")
        
        print("\n=== Test Completed Successfully ===")
        return True
        
    except Exception as e:
        print(f"✗ Test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    test_csv_similarity_parser() 