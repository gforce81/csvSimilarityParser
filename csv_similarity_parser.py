#!/usr/bin/env python3
"""
CSV Similarity Parser
A tool to compare two CSV files and create a third CSV with approval status based on exact row matches.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import os
from datetime import datetime
from difflib import SequenceMatcher
import threading


class CSVSimilarityParser:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Similarity Parser")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Data storage
        self.csv1_data = None
        self.csv2_data = None
        self.csv1_headers = []
        self.csv2_headers = []
        self.column_mappings = {}
        self.matching_columns = set()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # File selection section
        self.create_file_selection_section(main_frame)
        
        # Column mapping section
        self.create_mapping_section(main_frame)
        
        # Matching columns section
        self.create_matching_section(main_frame)
        
        # Approval column section
        self.create_approval_section(main_frame)
        
        # Process button
        self.create_process_section(main_frame)
        
        # Status section
        self.create_status_section(main_frame)
        
    def create_file_selection_section(self, parent):
        """Create the file selection section"""
        # File selection frame
        file_frame = ttk.LabelFrame(parent, text="File Selection", padding="10")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        # CSV 1 selection
        ttk.Label(file_frame, text="CSV 1 (Reference File):").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.csv1_path_var = tk.StringVar()
        csv1_entry = ttk.Entry(file_frame, textvariable=self.csv1_path_var, state='readonly')
        csv1_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        ttk.Button(file_frame, text="Browse", command=self.browse_csv1).grid(row=1, column=2, padx=(5, 0))
        
        # CSV 2 selection
        ttk.Label(file_frame, text="CSV 2 (File to Process):").grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        self.csv2_path_var = tk.StringVar()
        csv2_entry = ttk.Entry(file_frame, textvariable=self.csv2_path_var, state='readonly')
        csv2_entry.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        ttk.Button(file_frame, text="Browse", command=self.browse_csv2).grid(row=3, column=2, padx=(5, 0))
        
    def create_mapping_section(self, parent):
        """Create the column mapping section"""
        # Mapping frame
        mapping_frame = ttk.LabelFrame(parent, text="Column Mapping", padding="10")
        mapping_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        mapping_frame.columnconfigure(1, weight=1)
        
        # Instructions
        ttk.Label(mapping_frame, text="Map columns between CSV files (suggestions are automatic):").grid(
            row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        # Headers
        ttk.Label(mapping_frame, text="CSV 1 Column:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(mapping_frame, text="CSV 2 Column:").grid(row=1, column=1, sticky=tk.W)
        ttk.Label(mapping_frame, text="Action:").grid(row=1, column=2, sticky=tk.W)
        
        # Mapping listbox
        self.mapping_listbox = tk.Listbox(mapping_frame, height=8)
        self.mapping_listbox.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Mapping buttons
        mapping_buttons_frame = ttk.Frame(mapping_frame)
        mapping_buttons_frame.grid(row=2, column=2, padx=(10, 0), sticky=(tk.N, tk.S))
        
        ttk.Button(mapping_buttons_frame, text="Edit Mapping", command=self.edit_mapping).pack(pady=2)
        ttk.Button(mapping_buttons_frame, text="Remove Mapping", command=self.remove_mapping).pack(pady=2)
        ttk.Button(mapping_buttons_frame, text="Auto Map", command=self.auto_map_columns).pack(pady=2)
        ttk.Button(mapping_buttons_frame, text="Add Mapping", command=self.add_mapping).pack(pady=2)
        
    def create_matching_section(self, parent):
        """Create the matching columns section"""
        # Matching frame
        matching_frame = ttk.LabelFrame(parent, text="Matching Columns", padding="10")
        matching_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Instructions
        ttk.Label(matching_frame, text="Select columns to use for exact matching:").grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Matching checkboxes frame
        self.matching_checkboxes_frame = ttk.Frame(matching_frame)
        self.matching_checkboxes_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
    def create_approval_section(self, parent):
        """Create the matched status column section"""
        # Approval frame
        approval_frame = ttk.LabelFrame(parent, text="Matched Status Column", padding="10")
        approval_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        approval_frame.columnconfigure(1, weight=1)
        
        ttk.Label(approval_frame, text="Name for the new matched status column:").grid(row=0, column=0, sticky=tk.W)
        self.approval_column_var = tk.StringVar(value="Matched Status Column")
        ttk.Entry(approval_frame, textvariable=self.approval_column_var).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
    def create_process_section(self, parent):
        """Create the process button section"""
        # Process frame
        process_frame = ttk.Frame(parent)
        process_frame.grid(row=4, column=0, columnspan=2, pady=(0, 10))
        
        self.process_button = ttk.Button(process_frame, text="Process Files", command=self.process_files, state='disabled')
        self.process_button.pack()
        
    def create_status_section(self, parent):
        """Create the status section"""
        # Status frame
        status_frame = ttk.LabelFrame(parent, text="Status & Log", padding="10")
        status_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)
        parent.rowconfigure(5, weight=1)
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=8, wrap=tk.WORD)
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def browse_csv1(self):
        """Browse for CSV 1 file"""
        filename = filedialog.askopenfilename(
            title="Select CSV 1 (Reference File)",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.csv1_path_var.set(filename)
            self.load_csv1()
            
    def browse_csv2(self):
        """Browse for CSV 2 file"""
        filename = filedialog.askopenfilename(
            title="Select CSV 2 (File to Process)",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.csv2_path_var.set(filename)
            self.load_csv2()
            
    def load_csv1(self):
        """Load CSV 1 data"""
        try:
            self.csv1_data = pd.read_csv(self.csv1_path_var.get())
            self.csv1_headers = list(self.csv1_data.columns)
            self.log_message(f"Loaded CSV 1: {len(self.csv1_data)} rows, {len(self.csv1_headers)} columns")
            self.update_mapping_suggestions()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV 1: {str(e)}")
            
    def load_csv2(self):
        """Load CSV 2 data"""
        try:
            self.csv2_data = pd.read_csv(self.csv2_path_var.get())
            self.csv2_headers = list(self.csv2_data.columns)
            self.log_message(f"Loaded CSV 2: {len(self.csv2_data)} rows, {len(self.csv2_headers)} columns")
            self.update_mapping_suggestions()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV 2: {str(e)}")
            
    def update_mapping_suggestions(self):
        """Update column mapping suggestions"""
        if not self.csv1_headers or not self.csv2_headers:
            return
            
        self.auto_map_columns()
        self.update_process_button()
        
    def auto_map_columns(self):
        """Automatically suggest column mappings based on similarity"""
        self.column_mappings = {}
        
        for csv1_header in self.csv1_headers:
            best_match = None
            best_ratio = 0
            
            for csv2_header in self.csv2_headers:
                # Exact match
                if csv1_header.lower() == csv2_header.lower():
                    best_match = csv2_header
                    best_ratio = 1.0
                    break
                    
                # Similarity match
                ratio = SequenceMatcher(None, csv1_header.lower(), csv2_header.lower()).ratio()
                if ratio > best_ratio and ratio > 0.6:  # Threshold for similarity
                    best_ratio = ratio
                    best_match = csv2_header
            
            if best_match:
                self.column_mappings[csv1_header] = best_match
                
        self.update_mapping_display()
        self.update_matching_checkboxes()
        
    def update_mapping_display(self):
        """Update the mapping listbox display"""
        self.mapping_listbox.delete(0, tk.END)
        for csv1_header, csv2_header in self.column_mappings.items():
            self.mapping_listbox.insert(tk.END, f"{csv1_header} → {csv2_header}")
            
    def update_matching_checkboxes(self):
        """Update the matching checkboxes"""
        # Clear existing checkboxes
        for widget in self.matching_checkboxes_frame.winfo_children():
            widget.destroy()
            
        # Create new checkboxes for mapped columns
        self.matching_vars = {}
        row = 0
        col = 0
        max_cols = 3
        
        for csv1_header, csv2_header in self.column_mappings.items():
            var = tk.BooleanVar(value=True)  # Default to checked
            self.matching_vars[csv1_header] = var
            
            cb = ttk.Checkbutton(
                self.matching_checkboxes_frame,
                text=f"{csv1_header} ↔ {csv2_header}",
                variable=var
            )
            cb.grid(row=row, column=col, sticky=tk.W, padx=(0, 20), pady=2)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
                
    def edit_mapping(self):
        """Edit a selected mapping"""
        selection = self.mapping_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a mapping to edit")
            return
            
        index = selection[0]
        csv1_headers = list(self.column_mappings.keys())
        if index >= len(csv1_headers):
            return
            
        csv1_header = csv1_headers[index]
        current_mapping = self.column_mappings[csv1_header]
        
        # Create edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Mapping")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text=f"Map '{csv1_header}' to:").pack(pady=10)
        
        mapping_var = tk.StringVar(value=current_mapping)
        mapping_combo = ttk.Combobox(dialog, textvariable=mapping_var, values=self.csv2_headers, state='readonly')
        mapping_combo.pack(pady=10)
        
        def save_mapping():
            new_mapping = mapping_var.get()
            if new_mapping:
                self.column_mappings[csv1_header] = new_mapping
                self.update_mapping_display()
                self.update_matching_checkboxes()
            dialog.destroy()
            
        ttk.Button(dialog, text="Save", command=save_mapping).pack(pady=10)
        
    def remove_mapping(self):
        """Remove a selected mapping"""
        selection = self.mapping_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a mapping to remove")
            return
            
        index = selection[0]
        csv1_headers = list(self.column_mappings.keys())
        if index >= len(csv1_headers):
            return
            
        csv1_header = csv1_headers[index]
        del self.column_mappings[csv1_header]
        self.update_mapping_display()
        self.update_matching_checkboxes()
        
    def update_process_button(self):
        """Update the process button state"""
        if (self.csv1_data is not None and self.csv2_data is not None and 
            self.column_mappings and self.matching_vars):
            self.process_button.config(state='normal')
        else:
            self.process_button.config(state='disabled')
            
    def process_files(self):
        """Process the CSV files"""
        # Get selected matching columns
        self.matching_columns = set()
        for csv1_header, var in self.matching_vars.items():
            if var.get():
                self.matching_columns.add(csv1_header)
                
        if not self.matching_columns:
            messagebox.showwarning("Warning", "Please select at least one column for matching")
            return
            
        # Start processing in a separate thread
        thread = threading.Thread(target=self.process_files_thread)
        thread.daemon = True
        thread.start()
        
    def process_files_thread(self):
        """Process files in a separate thread"""
        try:
            self.log_message("Starting file processing...")
            self.process_button.config(state='disabled')
            
            # Create output data
            output_data = self.csv2_data.copy()
            
            # Add approval column
            approval_column_name = self.approval_column_var.get()
            output_data[approval_column_name] = "NO"
            
            # Create lookup set from CSV 1 for faster matching
            csv1_lookup = set()
            for _, row in self.csv1_data.iterrows():
                match_values = []
                for csv1_header in self.matching_columns:
                    csv2_header = self.column_mappings[csv1_header]
                    value = str(row[csv1_header]).strip()
                    match_values.append(value)
                csv1_lookup.add(tuple(match_values))
            
            self.log_message(f"Created lookup set with {len(csv1_lookup)} unique combinations")
            
            # Process CSV 2 rows
            matches_found = 0
            total_rows = len(output_data)
            
            for idx, row in output_data.iterrows():
                match_values = []
                for csv1_header in self.matching_columns:
                    csv2_header = self.column_mappings[csv1_header]
                    value = str(row[csv2_header]).strip()
                    match_values.append(value)
                
                if tuple(match_values) in csv1_lookup:
                    output_data.at[idx, approval_column_name] = "YES"
                    matches_found += 1
                    
                # Update progress every 1000 rows
                if (idx + 1) % 1000 == 0:
                    self.log_message(f"Processed {idx + 1}/{total_rows} rows...")
            
            # Generate output filename
            csv2_path = self.csv2_path_var.get()
            base_name = os.path.splitext(os.path.basename(csv2_path))[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{base_name}_with_matched_status_{timestamp}.csv"
            output_path = os.path.join(os.path.dirname(csv2_path), output_filename)
            
            # Save output file
            output_data.to_csv(output_path, index=False)
            
            self.log_message(f"Processing complete!")
            self.log_message(f"Total rows processed: {total_rows}")
            self.log_message(f"Matches found: {matches_found}")
            self.log_message(f"Output file: {output_path}")
            
            messagebox.showinfo("Success", f"Processing complete!\n\n"
                               f"Total rows: {total_rows}\n"
                               f"Matches found: {matches_found}\n"
                               f"Output saved to: {output_path}")
            
        except Exception as e:
            error_msg = f"Error during processing: {str(e)}"
            self.log_message(error_msg)
            messagebox.showerror("Error", error_msg)
        finally:
            self.process_button.config(state='normal')
            
    def log_message(self, message):
        """Add a message to the status log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Update GUI in main thread
        self.root.after(0, lambda: self.status_text.insert(tk.END, log_entry))
        self.root.after(0, lambda: self.status_text.see(tk.END))

    def add_mapping(self):
        """Add a new mapping between any CSV 1 and CSV 2 columns"""
        if not self.csv1_headers or not self.csv2_headers:
            messagebox.showwarning("Warning", "Please load both CSV files before adding a mapping.")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Add Mapping")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Select a column from CSV 1:").pack(pady=(10, 2))
        csv1_var = tk.StringVar()
        csv1_combo = ttk.Combobox(dialog, textvariable=csv1_var, values=self.csv1_headers, state='readonly')
        csv1_combo.pack(pady=5)

        ttk.Label(dialog, text="Select a column from CSV 2:").pack(pady=(10, 2))
        csv2_var = tk.StringVar()
        csv2_combo = ttk.Combobox(dialog, textvariable=csv2_var, values=self.csv2_headers, state='readonly')
        csv2_combo.pack(pady=5)

        def save_mapping():
            csv1_col = csv1_var.get()
            csv2_col = csv2_var.get()
            if not csv1_col or not csv2_col:
                messagebox.showwarning("Warning", "Please select both columns.")
                return
            self.column_mappings[csv1_col] = csv2_col
            self.update_mapping_display()
            self.update_matching_checkboxes()
            dialog.destroy()

        ttk.Button(dialog, text="Add Mapping", command=save_mapping).pack(pady=15)


def main():
    """Main function"""
    root = tk.Tk()
    app = CSVSimilarityParser(root)
    root.mainloop()


if __name__ == "__main__":
    main() 