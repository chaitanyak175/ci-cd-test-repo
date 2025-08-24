# Web Scraper with security and performance issues
import urllib.request  # Old, should use requests
import ssl
import time
import re
from html.parser import HTMLParser

class WebScraper:
    def __init__(self):
        # Disabling SSL verification - SECURITY RISK
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
    
    def fetch_url(self, url: str) -> str:
        """Fetch URL with security vulnerabilities"""
        # No URL validation - could be exploited
        # No rate limiting
        # Using deprecated urllib instead of requests
        
        try:
            request = urllib.request.Request(url)
            # Missing User-Agent header - might be blocked
            
            with urllib.request.urlopen(request, context=self.ssl_context, timeout=30) as response:
                content = response.read().decode('utf-8')
                return content
                
        except Exception as e:
            # Too broad exception handling
            print(f"Error: {e}")
            return ""
    
    def extract_emails(self, html_content: str) -> list:
        """Extract emails with vulnerable regex"""
        # Vulnerable to ReDoS (Regular Expression Denial of Service)
        email_pattern = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)*'
        
        emails = re.findall(email_pattern, html_content)
        return emails
    
    def extract_links(self, html_content: str, base_url: str) -> list:
        """Extract links without proper URL validation"""
        link_pattern = r'href=["\']([^"\']+)["\']'
        links = re.findall(link_pattern, html_content)
        
        absolute_links = []
        for link in links:
            # No validation for malicious URLs
            if link.startswith('http'):
                absolute_links.append(link)
            else:
                # Simple concatenation - could create invalid URLs
                absolute_url = base_url + link
                absolute_links.append(absolute_url)
        
        return absolute_links
    
    def scrape_multiple_urls(self, urls: list) -> dict:
        """Scrape multiple URLs without concurrency or rate limiting"""
        results = {}
        
        for url in urls:
            # No rate limiting - could get IP banned
            # No concurrent processing - very slow
            content = self.fetch_url(url)
            results[url] = content
            
            # Fixed delay regardless of server response
            time.sleep(1)  # Inefficient, should be adaptive
        
        return results
    
    def save_content(self, content: str, filename: str):
        """Save content with path traversal vulnerability"""
        # No path sanitization - vulnerable to path traversal
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def parse_html_table(self, html_content: str) -> list:
        """Parse HTML table without proper parsing"""
        # Using regex for HTML parsing - unreliable and dangerous
        table_pattern = r'<table.*?>(.*?)</table>'
        row_pattern = r'<tr.*?>(.*?)</tr>'
        cell_pattern = r'<td.*?>(.*?)</td>'
        
        tables = re.findall(table_pattern, html_content, re.DOTALL)
        
        parsed_tables = []
        for table in tables:
            rows = re.findall(row_pattern, table, re.DOTALL)
            parsed_rows = []
            
            for row in rows:
                cells = re.findall(cell_pattern, row, re.DOTALL)
                # No HTML entity decoding
                parsed_rows.append(cells)
            
            parsed_tables.append(parsed_rows)
        
        return parsed_tables
    
    def download_image(self, image_url: str, local_path: str):
        """Download image with no size or type validation"""
        # No file size limit - could download huge files
        # No file type validation - could download malicious files
        # No disk space check
        
        try:
            urllib.request.urlretrieve(image_url, local_path)
        except:
            # Silent failure
            pass
    
    def extract_forms(self, html_content: str) -> list:
        """Extract forms without security considerations"""
        form_pattern = r'<form.*?>(.*?)</form>'
        forms = re.findall(form_pattern, html_content, re.DOTALL | re.IGNORECASE)
        
        form_data = []
        for form in forms:
            # Extract inputs without validation
            input_pattern = r'<input.*?name=["\']([^"\']+)["\'].*?>'
            inputs = re.findall(input_pattern, form, re.IGNORECASE)
            form_data.append(inputs)
        
        return form_data

class HTMLTableParser(HTMLParser):
    """HTML parser with missing error handling"""
    def __init__(self):
        super().__init__()
        self.tables = []
        self.current_table = []
        self.current_row = []
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.cell_data = ""
    
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.in_table = True
            self.current_table = []
        elif tag == 'tr' and self.in_table:
            self.in_row = True
            self.current_row = []
        elif tag == 'td' and self.in_row:
            self.in_cell = True
            self.cell_data = ""
    
    def handle_endtag(self, tag):
        if tag == 'table':
            self.in_table = False
            self.tables.append(self.current_table)
        elif tag == 'tr' and self.in_table:
            self.in_row = False
            self.current_table.append(self.current_row)
        elif tag == 'td' and self.in_row:
            self.in_cell = False
            self.current_row.append(self.cell_data.strip())
    
    def handle_data(self, data):
        if self.in_cell:
            self.cell_data += data

# Dangerous usage example
if __name__ == "__main__":
    scraper = WebScraper()
    
    # Could be exploited with malicious URLs
    suspicious_urls = [
        "http://malicious-site.com/../../etc/passwd",
        "javascript:alert('xss')",
        "file:///etc/passwd"
    ]
    
    # This will attempt to scrape potentially dangerous URLs
    for url in suspicious_urls:
        content = scraper.fetch_url(url)
        scraper.save_content(content, f"scraped_{url.replace('/', '_')}.html")
