# Security-focused tests for web scraper
import unittest
import sys
import os
import tempfile
from unittest.mock import patch, Mock, MagicMock

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from web_scraper import WebScraper, HTMLTableParser
except ImportError as e:
    print(f"Import error: {e}")


class TestWebScraperSecurity(unittest.TestCase):
    """Security-focused tests for WebScraper"""
    
    def setUp(self):
        """Set up test environment"""
        try:
            self.scraper = WebScraper()
        except Exception as e:
            self.scraper = None
            print(f"Failed to create scraper: {e}")
    
    def test_ssl_verification_disabled(self):
        """Test that SSL verification is dangerously disabled"""
        if self.scraper is None:
            self.skipTest("Scraper not available")
        
        import ssl
        
        # Check SSL context settings
        self.assertFalse(self.scraper.ssl_context.check_hostname)
        self.assertEqual(self.scraper.ssl_context.verify_mode, ssl.CERT_NONE)
        
        print("WARNING: SSL verification is disabled - security vulnerability!")
    
    def test_url_validation_missing(self):
        """Test lack of URL validation allows malicious URLs"""
        if self.scraper is None:
            self.skipTest("Scraper not available")
        
        malicious_urls = [
            "file:///etc/passwd",  # Local file access
            "javascript:alert('xss')",  # JavaScript injection
            "data:text/html,<script>alert('xss')</script>",  # Data URL
            "ftp://malicious.com/../../etc/passwd",  # FTP with path traversal
        ]
        
        for url in malicious_urls:
            # The scraper should reject these URLs but doesn't
            try:
                result = self.scraper.fetch_url(url)
                print(f"WARNING: Malicious URL '{url}' was not blocked")
            except Exception as e:
                print(f"URL '{url}' properly blocked: {e}")
    
    @patch('urllib.request.urlopen')
    def test_missing_rate_limiting(self, mock_urlopen):
        """Test lack of rate limiting"""
        if self.scraper is None:
            self.skipTest("Scraper not available")
        
        # Mock response
        mock_response = Mock()
        mock_response.read.return_value = b"<html><body>Test</body></html>"
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = None
        mock_urlopen.return_value = mock_response
        
        urls = ["http://example.com"] * 100  # 100 rapid requests
        
        import time
        start_time = time.time()
        
        results = self.scraper.scrape_multiple_urls(urls)
        
        end_time = time.time()
        
        # Check if rate limiting is applied
        expected_min_time = len(urls) * 1  # 1 second per request
        actual_time = end_time - start_time
        
        print(f"Scraped {len(urls)} URLs in {actual_time:.2f} seconds")
        print(f"Expected minimum time with rate limiting: {expected_min_time} seconds")
        
        # This reveals the fixed 1-second delay regardless of server response
        self.assertGreaterEqual(actual_time, expected_min_time * 0.9)
    
    def test_path_traversal_vulnerability(self):
        """Test path traversal vulnerability in save_content"""
        if self.scraper is None:
            self.skipTest("Scraper not available")
        
        malicious_filenames = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "/etc/shadow",
            "C:\\Windows\\System32\\config\\SAM",
        ]
        
        for filename in malicious_filenames:
            try:
                # This should not allow writing to arbitrary paths
                self.scraper.save_content("test content", filename)
                print(f"WARNING: Path traversal possible with filename: {filename}")
            except Exception as e:
                print(f"Path traversal blocked for '{filename}': {e}")
    
    def test_redos_vulnerability(self):
        """Test Regular Expression Denial of Service vulnerability"""
        if self.scraper is None:
            self.skipTest("Scraper not available")
        
        # Crafted input that could cause ReDoS
        malicious_input = "a" * 10000 + "@" + "b" * 10000
        
        import time
        start_time = time.time()
        
        try:
            emails = self.scraper.extract_emails(malicious_input)
            end_time = time.time()
            
            execution_time = end_time - start_time
            print(f"Email extraction took {execution_time:.4f} seconds")
            
            # If it takes too long, it might be vulnerable to ReDoS
            if execution_time > 1.0:
                print("WARNING: Possible ReDoS vulnerability detected!")
        except Exception as e:
            print(f"Email extraction failed: {e}")
    
    def test_html_parsing_with_regex(self):
        """Test dangerous HTML parsing with regex"""
        if self.scraper is None:
            self.skipTest("Scraper not available")
        
        # Malicious HTML that could exploit regex parsing
        malicious_html = """
        <table>
            <tr><td>Normal data</td></tr>
            <tr><td onclick="javascript:alert('xss')">Malicious</td></tr>
            <tr><td><script>alert('More XSS')</script></td></tr>
        </table>
        """
        
        try:
            tables = self.scraper.parse_html_table(malicious_html)
            
            # Check if malicious content is properly handled
            for table in tables:
                for row in table:
                    for cell in row:
                        if 'javascript:' in cell or '<script>' in cell:
                            print(f"WARNING: Malicious content not sanitized: {cell}")
        except Exception as e:
            print(f"HTML parsing failed: {e}")
    
    def test_file_download_vulnerabilities(self):
        """Test file download security issues"""
        if self.scraper is None:
            self.skipTest("Scraper not available")
        
        # Test with various file types and sizes
        test_cases = [
            {
                'url': 'http://example.com/huge-file.zip',
                'description': 'Large file (no size limit)'
            },
            {
                'url': 'http://example.com/malware.exe',
                'description': 'Executable file (no type validation)'
            },
            {
                'url': 'http://example.com/../../../etc/passwd',
                'description': 'Path traversal in URL'
            }
        ]
        
        for test_case in test_cases:
            try:
                # Mock the download to avoid actually downloading
                with patch('urllib.request.urlretrieve') as mock_download:
                    self.scraper.download_image(test_case['url'], 'test_file')
                    print(f"WARNING: {test_case['description']} - not blocked")
            except Exception as e:
                print(f"Download blocked for {test_case['description']}: {e}")
    
    def test_user_agent_missing(self):
        """Test missing User-Agent header"""
        if self.scraper is None:
            self.skipTest("Scraper not available")
        
        with patch('urllib.request.Request') as mock_request:
            self.scraper.fetch_url("http://example.com")
            
            # Check if User-Agent header was added
            call_args = mock_request.call_args
            if call_args:
                headers = call_args[1].get('headers', {}) if len(call_args) > 1 else {}
                if 'User-Agent' not in headers:
                    print("WARNING: No User-Agent header - might be blocked by servers")


class TestWebScraperPerformance(unittest.TestCase):
    """Performance and efficiency tests"""
    
    def setUp(self):
        try:
            self.scraper = WebScraper()
        except:
            self.scraper = None
    
    def test_synchronous_operations(self):
        """Test inefficient synchronous operations"""
        if self.scraper is None:
            self.skipTest("Scraper not available")
        
        urls = [f"http://example.com/page{i}" for i in range(10)]
        
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = Mock()
            mock_response.read.return_value = b"<html><body>Test</body></html>"
            mock_response.__enter__.return_value = mock_response
            mock_response.__exit__.return_value = None
            mock_urlopen.return_value = mock_response
            
            import time
            start_time = time.time()
            
            results = self.scraper.scrape_multiple_urls(urls)
            
            end_time = time.time()
            total_time = end_time - start_time
            
            print(f"Sequential scraping of {len(urls)} URLs took {total_time:.2f} seconds")
            print("This could be much faster with concurrent processing")
            
            self.assertEqual(len(results), len(urls))
    
    def test_memory_usage_html_parsing(self):
        """Test memory usage with large HTML content"""
        if self.scraper is None:
            self.skipTest("Scraper not available")
        
        # Generate large HTML content
        large_html = "<html><body>"
        for i in range(10000):
            large_html += f"<p>This is paragraph {i} with some content</p>"
        large_html += "</body></html>"
        
        import sys
        
        # Measure memory usage
        try:
            size_before = sys.getsizeof(large_html)
            
            links = self.scraper.extract_links(large_html, "http://example.com")
            
            print(f"Processed HTML of size {size_before} bytes")
            print(f"Found {len(links)} links")
            
        except Exception as e:
            print(f"Large HTML processing failed: {e}")


class TestHTMLTableParser(unittest.TestCase):
    """Tests for HTML table parser"""
    
    def setUp(self):
        try:
            self.parser = HTMLTableParser()
        except:
            self.parser = None
    
    def test_malformed_html_handling(self):
        """Test handling of malformed HTML"""
        if self.parser is None:
            self.skipTest("Parser not available")
        
        malformed_html_cases = [
            "<table><tr><td>Unclosed cell",
            "<table><tr>Missing cell tags</tr></table>",
            "<table><td>Cell without row</td></table>",
            "<table><tr><td>Nested <table><tr><td>table</td></tr></table></td></tr></table>",
        ]
        
        for html in malformed_html_cases:
            try:
                self.parser.feed(html)
                print(f"Malformed HTML handled: {html[:30]}...")
            except Exception as e:
                print(f"Parser failed on malformed HTML: {e}")
    
    def test_xss_in_table_content(self):
        """Test XSS prevention in table parsing"""
        if self.parser is None:
            self.skipTest("Parser not available")
        
        xss_html = """
        <table>
            <tr>
                <td><script>alert('XSS')</script></td>
                <td onclick="alert('Click XSS')">Click me</td>
                <td><img src="x" onerror="alert('Image XSS')"></td>
            </tr>
        </table>
        """
        
        try:
            self.parser.feed(xss_html)
            
            # Check if XSS content is in the parsed data
            for table in self.parser.tables:
                for row in table:
                    for cell in row:
                        if any(xss_pattern in cell for xss_pattern in ['<script>', 'onclick=', 'onerror=']):
                            print(f"WARNING: XSS content not sanitized: {cell}")
        except Exception as e:
            print(f"XSS test failed: {e}")


class TestWebScraperRobustness(unittest.TestCase):
    """Robustness and error handling tests"""
    
    def setUp(self):
        try:
            self.scraper = WebScraper()
        except:
            self.scraper = None
    
    def test_network_timeout_handling(self):
        """Test handling of network timeouts"""
        if self.scraper is None:
            self.skipTest("Scraper not available")
        
        with patch('urllib.request.urlopen') as mock_urlopen:
            # Simulate timeout
            mock_urlopen.side_effect = TimeoutError("Request timed out")
            
            result = self.scraper.fetch_url("http://slow-server.com")
            
            # Should return empty string on timeout
            self.assertEqual(result, "")
    
    def test_invalid_encoding_handling(self):
        """Test handling of invalid character encoding"""
        if self.scraper is None:
            self.skipTest("Scraper not available")
        
        with patch('urllib.request.urlopen') as mock_urlopen:
            # Mock response with invalid UTF-8
            mock_response = Mock()
            mock_response.read.return_value = b'\xff\xfe\x00\x00invalid utf-8'
            mock_response.__enter__.return_value = mock_response
            mock_response.__exit__.return_value = None
            mock_urlopen.return_value = mock_response
            
            try:
                result = self.scraper.fetch_url("http://example.com")
                print("Invalid encoding handled gracefully")
            except UnicodeDecodeError:
                print("WARNING: Invalid encoding not handled properly")


if __name__ == "__main__":
    # Run all security tests
    unittest.main(verbosity=2, warnings='ignore')
