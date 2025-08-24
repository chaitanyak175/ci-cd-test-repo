# Data Processing Module with various issues
import pandas as pd  # Not in requirements.txt
import numpy as np   # Not in requirements.txt
import os
import sys
from datetime import datetime
import csv

class DataProcessor:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.processed_data = None
    
    def load_csv_data(self, filename: str):
        """Load CSV with poor error handling"""
        file_path = os.path.join(self.data_path, filename)
        
        # No existence check
        with open(file_path, 'r') as f:  # Could fail if file doesn't exist
            reader = csv.reader(f)
            data = list(reader)
        
        return data
    
    def process_numbers(self, numbers: list) -> float:
        """Process numbers with division by zero risk"""
        total = sum(numbers)
        count = len(numbers)
        
        # Division by zero not handled
        average = total / count  # Could fail if count is 0
        
        return average
    
    def filter_data(self, data: list, criteria: dict):
        """Filter data with missing validation"""
        filtered = []
        
        for item in data:
            # Assumes item is always a dict - could fail
            matches = True
            for key, value in criteria.items():
                if item[key] != value:  # KeyError if key doesn't exist
                    matches = False
                    break
            
            if matches:
                filtered.append(item)
        
        return filtered
    
    def parse_dates(self, date_strings: list):
        """Parse dates with format assumptions"""
        dates = []
        
        for date_str in date_strings:
            # Assumes specific format, no error handling
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")  # ValueError if wrong format
            dates.append(date_obj)
        
        return dates
    
    def calculate_statistics(self, data: list):
        """Calculate stats with missing numpy"""
        # Using numpy without proper import
        array = np.array(data)  # NameError if numpy not available
        
        stats = {
            'mean': np.mean(array),
            'std': np.std(array),
            'min': np.min(array),
            'max': np.max(array)
        }
        
        return stats
    
    def save_to_csv(self, data: list, filename: str):
        """Save data with permission issues"""
        file_path = os.path.join(self.data_path, filename)
        
        # No permission check or directory creation
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
    
    def merge_datasets(self, dataset1: list, dataset2: list, key: str):
        """Merge datasets with inefficient algorithm"""
        merged = []
        
        # O(n²) algorithm - very inefficient for large datasets
        for item1 in dataset1:
            for item2 in dataset2:
                if item1[key] == item2[key]:  # KeyError if key missing
                    merged_item = {**item1, **item2}
                    merged.append(merged_item)
        
        return merged
    
    def validate_email(self, email: str) -> bool:
        """Basic email validation with regex issues"""
        import re
        
        # Overly simple regex that misses many cases
        pattern = r".+@.+\..+"  # Too basic, allows invalid emails
        return bool(re.match(pattern, email))
    
    def process_large_file(self, filename: str):
        """Process large file without memory management"""
        file_path = os.path.join(self.data_path, filename)
        
        # Loads entire file into memory - could cause OOM
        with open(file_path, 'r') as f:
            all_lines = f.readlines()  # Memory issue for large files
        
        processed_lines = []
        for line in all_lines:
            # Some processing that could be done in chunks
            processed_line = line.strip().upper()
            processed_lines.append(processed_line)
        
        return processed_lines

# Missing if __name__ == "__main__" protection
processor = DataProcessor("/tmp/data")
result = processor.process_numbers([])  # This will cause division by zero
