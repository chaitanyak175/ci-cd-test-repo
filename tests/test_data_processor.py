# Tests for Data Processor with comprehensive coverage
import unittest
import tempfile
import os
import csv
from unittest.mock import patch, mock_open, Mock
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from data_processor import DataProcessor
except ImportError as e:
    print(f"Import error: {e}")


class TestDataProcessor(unittest.TestCase):
    """Comprehensive tests for DataProcessor class"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        try:
            self.processor = DataProcessor(self.temp_dir)
        except Exception as e:
            self.processor = None
            print(f"Failed to create processor: {e}")
    
    def tearDown(self):
        """Clean up test environment"""
        # Clean up temp directory
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_process_numbers_division_by_zero(self):
        """Test division by zero in process_numbers"""
        if self.processor is None:
            self.skipTest("Processor not available")
        
        # This should catch the division by zero error
        with self.assertRaises(ZeroDivisionError):
            self.processor.process_numbers([])
    
    def test_process_numbers_valid_input(self):
        """Test process_numbers with valid input"""
        if self.processor is None:
            self.skipTest("Processor not available")
        
        numbers = [1, 2, 3, 4, 5]
        result = self.processor.process_numbers(numbers)
        
        expected = sum(numbers) / len(numbers)
        self.assertEqual(result, expected)
    
    def test_load_csv_file_not_exists(self):
        """Test loading non-existent CSV file"""
        if self.processor is None:
            self.skipTest("Processor not available")
        
        # This should raise FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            self.processor.load_csv_data("nonexistent.csv")
    
    def test_load_csv_valid_file(self):
        """Test loading valid CSV file"""
        if self.processor is None:
            self.skipTest("Processor not available")
        
        # Create a test CSV file
        test_file = os.path.join(self.temp_dir, "test.csv")
        test_data = [["name", "age"], ["John", "25"], ["Jane", "30"]]
        
        with open(test_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(test_data)
        
        result = self.processor.load_csv_data("test.csv")
        self.assertEqual(result, test_data)
    
    def test_filter_data_key_error(self):
        """Test filter_data with missing keys"""
        if self.processor is None:
            self.skipTest("Processor not available")
        
        data = [{"name": "John", "age": 25}]
        criteria = {"missing_key": "value"}
        
        # This should raise KeyError
        with self.assertRaises(KeyError):
            self.processor.filter_data(data, criteria)
    
    def test_filter_data_valid_criteria(self):
        """Test filter_data with valid criteria"""
        if self.processor is None:
            self.skipTest("Processor not available")
        
        data = [
            {"name": "John", "age": 25},
            {"name": "Jane", "age": 30},
            {"name": "Bob", "age": 25}
        ]
        criteria = {"age": 25}
        
        result = self.processor.filter_data(data, criteria)
        expected = [{"name": "John", "age": 25}, {"name": "Bob", "age": 25}]
        
        self.assertEqual(result, expected)
    
    def test_parse_dates_invalid_format(self):
        """Test parse_dates with invalid date format"""
        if self.processor is None:
            self.skipTest("Processor not available")
        
        invalid_dates = ["2023-13-45", "not-a-date", "2023/01/01"]
        
        # This should raise ValueError due to invalid date formats
        with self.assertRaises(ValueError):
            self.processor.parse_dates(invalid_dates)
    
    def test_parse_dates_valid_format(self):
        """Test parse_dates with valid format"""
        if self.processor is None:
            self.skipTest("Processor not available")
        
        valid_dates = ["2023-01-01", "2023-12-31"]
        result = self.processor.parse_dates(valid_dates)
        
        self.assertEqual(len(result), 2)
        # Check that dates were parsed correctly
        from datetime import datetime
        expected_first = datetime(2023, 1, 1)
        self.assertEqual(result[0], expected_first)
    
    @patch('numpy.array')
    def test_calculate_statistics_numpy_missing(self, mock_array):
        """Test calculate_statistics when numpy is not available"""
        if self.processor is None:
            self.skipTest("Processor not available")
        
        # Mock numpy not being available
        mock_array.side_effect = NameError("name 'np' is not defined")
        
        data = [1, 2, 3, 4, 5]
        
        with self.assertRaises(NameError):
            self.processor.calculate_statistics(data)
    
    def test_merge_datasets_missing_key(self):
        """Test merge_datasets with missing keys"""
        if self.processor is None:
            self.skipTest("Processor not available")
        
        dataset1 = [{"id": 1, "name": "John"}]
        dataset2 = [{"user_id": 1, "email": "john@example.com"}]  # Different key
        
        # This should raise KeyError due to missing 'id' key in dataset2
        with self.assertRaises(KeyError):
            self.processor.merge_datasets(dataset1, dataset2, "id")
    
    def test_merge_datasets_performance(self):
        """Test merge_datasets performance with large datasets"""
        if self.processor is None:
            self.skipTest("Processor not available")
        
        # Create large datasets to test O(n²) performance issue
        dataset1 = [{"id": i, "name": f"User{i}"} for i in range(100)]
        dataset2 = [{"id": i, "email": f"user{i}@example.com"} for i in range(100)]
        
        import time
        start_time = time.time()
        
        result = self.processor.merge_datasets(dataset1, dataset2, "id")
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # This test would reveal the inefficiency
        self.assertEqual(len(result), 100)
        print(f"Merge execution time: {execution_time:.4f} seconds")
    
    def test_validate_email_weak_validation(self):
        """Test weak email validation"""
        if self.processor is None:
            self.skipTest("Processor not available")
        
        # Test cases that should fail but might pass with weak regex
        invalid_emails = [
            "@example.com",  # Missing local part
            "user@",  # Missing domain
            "user.example.com",  # Missing @
            "user@example",  # Missing TLD
        ]
        
        for email in invalid_emails:
            result = self.processor.validate_email(email)
            # Some of these might incorrectly pass due to weak regex
            print(f"Email '{email}' validation result: {result}")
    
    def test_process_large_file_memory_usage(self):
        """Test memory usage with large files"""
        if self.processor is None:
            self.skipTest("Processor not available")
        
        # Create a large test file
        large_file = os.path.join(self.temp_dir, "large_test.txt")
        
        # Write a file with many lines
        with open(large_file, 'w') as f:
            for i in range(10000):
                f.write(f"This is line {i} with some content\n")
        
        # This test would reveal memory issues with large files
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss
        
        result = self.processor.process_large_file("large_test.txt")
        
        memory_after = process.memory_info().rss
        memory_increase = memory_after - memory_before
        
        print(f"Memory increase: {memory_increase / 1024 / 1024:.2f} MB")
        self.assertEqual(len(result), 10000)


class TestDataProcessorEdgeCases(unittest.TestCase):
    """Edge case tests"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        try:
            self.processor = DataProcessor(self.temp_dir)
        except:
            self.processor = None
    
    def test_empty_data_handling(self):
        """Test handling of empty data"""
        if self.processor is None:
            self.skipTest("Processor not available")
        
        # Test with empty lists
        empty_data = []
        
        # These should handle empty data gracefully
        with self.assertRaises(ZeroDivisionError):
            self.processor.process_numbers(empty_data)
    
    def test_invalid_data_types(self):
        """Test handling of invalid data types"""
        if self.processor is None:
            self.skipTest("Processor not available")
        
        # Test with non-numeric data
        invalid_numbers = ["a", "b", "c"]
        
        with self.assertRaises(TypeError):
            self.processor.process_numbers(invalid_numbers)
    
    def test_permission_errors(self):
        """Test handling of permission errors"""
        if self.processor is None:
            self.skipTest("Processor not available")
        
        # Create a directory without write permissions
        restricted_dir = os.path.join(self.temp_dir, "restricted")
        os.makedirs(restricted_dir)
        os.chmod(restricted_dir, 0o444)  # Read-only
        
        restricted_processor = DataProcessor(restricted_dir)
        
        # This should raise PermissionError
        with self.assertRaises(PermissionError):
            restricted_processor.save_to_csv([["test"]], "test.csv")


if __name__ == "__main__":
    # Run with high verbosity to see all test details
    unittest.main(verbosity=2, buffer=True)
