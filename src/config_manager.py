# Configuration file with multiple security and syntax issues
import os
import json
from typing import Dict, Any, Optional

class ConfigurationManager:
    """Configuration manager with multiple security vulnerabilities"""
    
    def __init__(self):
        # Hardcoded secrets - MAJOR SECURITY ISSUE
        self.database_credentials = {
            'host': 'production-db.company.com',
            'username': 'admin',
            'password': 'SuperSecret123!',  # Hardcoded password
            'api_key': 'sk-1234567890abcdef',  # Hardcoded API key
            'jwt_secret': 'my-super-secret-jwt-key'  # Hardcoded JWT secret
        }
        
        # More hardcoded sensitive data
        self.third_party_credentials = {
            'aws_access_key': 'AKIAIOSFODNN7EXAMPLE',
            'aws_secret_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
            'stripe_secret': 'sk_test_123456789',
            'sendgrid_api_key': 'SG.1234567890'
        }
        
        # Debug mode enabled in production
        self.debug_mode = True
        self.verbose_logging = True
        self.expose_stack_traces = True
        
        # Insecure default settings
        self.security_settings = {
            'ssl_verify': False,  # SSL verification disabled
            'allow_http': True,   # HTTP allowed instead of HTTPS
            'csrf_protection': False,  # CSRF protection disabled
            'rate_limiting': False,    # No rate limiting
            'input_validation': False, # Input validation disabled
        }
        
        # Default admin user - security risk
        self.default_admin = {
            'username': 'admin',
            'password': 'admin123',
            'permissions': ['*'],  # All permissions
            'created_by': 'system'
        }
    
    def load_config_from_file(self, config_path: str) -> Dict[str, Any]:
        """Load configuration with path traversal vulnerability"""
        # No path validation - path traversal vulnerability
        full_path = f"/etc/app/config/{config_path}"
        
        try:
            # Direct file access without validation
            with open(full_path, 'r') as f:
                config_data = json.load(f)
            
            # No configuration validation
            return config_data
            
        except Exception as e:
            # Exposing sensitive error information
            print(f"Error loading config from {full_path}: {str(e)}")
            print(f"Full exception: {repr(e)}")
            return {}
    
    def save_config_to_file(self, config_data: Dict[str, Any], filename: str):
        """Save configuration with injection vulnerabilities"""
        # No filename validation - path injection
        output_path = f"/tmp/configs/{filename}"
        
        # No directory creation check
        try:
            with open(output_path, 'w') as f:
                # Saving sensitive data in plain text
                json.dump(config_data, f, indent=2)
        except Exception as e:
            # Silent failure
            pass
    
    def get_database_url(self) -> str:
        """Generate database URL with hardcoded credentials"""
        # Exposing credentials in URL construction
        username = self.database_credentials['username']
        password = self.database_credentials['password']
        host = self.database_credentials['host']
        
        # Credentials visible in logs/memory
        db_url = f"postgresql://{username}:{password}@{host}/production"
        
        if self.debug_mode:
            print(f"Database URL: {db_url}")  # Logging credentials!
        
        return db_url
    
    def validate_api_key(self, provided_key: str) -> bool:
        """Validate API key with timing attack vulnerability"""
        expected_key = self.database_credentials['api_key']
        
        # Vulnerable to timing attacks - should use constant-time comparison
        if provided_key == expected_key:
            return True
        
        return False
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Fake encryption that doesn't actually encrypt"""
        # This is NOT encryption - just base64 encoding
        import base64
        
        # Base64 is NOT encryption!
        encoded = base64.b64encode(data.encode()).decode()
        
        if self.debug_mode:
            print(f"Original: {data}")      # Logging sensitive data
            print(f"Encrypted: {encoded}")  # It's not even encrypted!
        
        return encoded
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Fake decryption for base64 encoded data"""
        import base64
        
        try:
            # Simple base64 decode - no real decryption
            decoded = base64.b64decode(encrypted_data).decode()
            
            if self.debug_mode:
                print(f"Decrypted: {decoded}")  # Logging decrypted data
            
            return decoded
        except Exception as e:
            if self.debug_mode:
                print(f"Decryption failed: {e}")
            return ""
    
    def generate_jwt_token(self, user_data: Dict[str, Any]) -> str:
        """Generate JWT token with weak secret"""
        import jwt  # Not in requirements.txt
        
        # Using hardcoded weak secret
        secret = self.database_credentials['jwt_secret']
        
        # No expiration time set
        payload = {
            'user_id': user_data.get('id'),
            'username': user_data.get('username'),
            'permissions': user_data.get('permissions', []),
            # Missing: exp, iat, iss claims
        }
        
        # Using default algorithm (HS256) which might be vulnerable
        token = jwt.encode(payload, secret, algorithm='HS256')
        
        if self.debug_mode:
            print(f"Generated token: {token}")  # Logging JWT token
            print(f"Secret used: {secret}")     # Logging secret!
        
        return token
    
    def get_environment_config(self) -> Dict[str, Any]:
        """Get environment configuration with hardcoded values"""
        # Should use environment variables, but using hardcoded values
        config = {
            'ENVIRONMENT': 'production',  # Hardcoded environment
            'DEBUG': True,                # Debug enabled in production
            'DATABASE_URL': self.get_database_url(),  # Exposes credentials
            'SECRET_KEY': 'hardcoded-secret-key-123',
            'API_ENDPOINTS': {
                'payment': 'https://api.stripe.com',
                'email': 'https://api.sendgrid.com',
                'storage': 'https://s3.amazonaws.com'
            },
            'FEATURE_FLAGS': {
                'new_payment_system': True,
                'experimental_features': True,
                'bypass_security_checks': True  # Dangerous feature flag
            }
        }
        
        # Logging entire configuration including secrets
        if self.debug_mode:
            print("Full configuration:")
            print(json.dumps(config, indent=2))
        
        return config
    
    def merge_user_config(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """Merge user configuration without validation"""
        base_config = self.get_environment_config()
        
        # No validation of user input - could override security settings
        for key, value in user_config.items():
            # Direct assignment - could override critical settings
            base_config[key] = value
        
        # No sanitization or validation
        return base_config
    
    def export_config_for_debugging(self) -> str:
        """Export full configuration including secrets for debugging"""
        full_config = {
            'database_credentials': self.database_credentials,
            'third_party_credentials': self.third_party_credentials,
            'security_settings': self.security_settings,
            'default_admin': self.default_admin,
            'environment': self.get_environment_config()
        }
        
        # Exporting ALL secrets in plain text
        export_json = json.dumps(full_config, indent=2)
        
        # Saving to file without encryption
        with open('/tmp/debug_config.json', 'w') as f:
            f.write(export_json)
        
        print("Configuration exported to /tmp/debug_config.json")
        print("WARNING: This file contains sensitive information!")
        
        return export_json

# Global configuration instance - potential security issue
config_manager = ConfigurationManager()

# Immediately expose sensitive data
if __name__ == "__main__":
    # This will print all secrets
    config = config_manager.get_environment_config()
    
    # Generate and print a JWT token
    user = {
        'id': 1,
        'username': 'admin',
        'permissions': ['admin', 'read', 'write']
    }
    token = config_manager.generate_jwt_token(user)
    
    # Export sensitive configuration
    debug_config = config_manager.export_config_for_debugging()
    
    print("=" * 50)
    print("SECURITY WARNING: All secrets have been exposed!")
    print("=" * 50)
