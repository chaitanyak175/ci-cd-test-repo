// JavaScript module with multiple issues
const fs = require('fs');
const path = require('path');
const crypto = require('crypto'); // Missing in package.json
const request = require('request'); // Deprecated package

class DatabaseManager {
    constructor(connectionString) {
        this.connectionString = connectionString;
        this.connection = null;
        
        // Hardcoded credentials - SECURITY ISSUE
        this.defaultCredentials = {
            username: 'admin',
            password: 'password123',
            host: 'localhost'
        };
    }
    
    // Missing async/await, using callbacks incorrectly
    connect(callback) {
        // Simulating database connection with security issues
        setTimeout(() => {
            if (this.connectionString.includes('localhost')) {
                this.connection = { status: 'connected' };
                callback(null, this.connection);
            } else {
                callback(new Error('Connection failed'));
            }
        }, 100);
    }
    
    // SQL injection vulnerability
    queryUser(userId, callback) {
        // Direct string concatenation - SQL injection risk
        const query = `SELECT * FROM users WHERE id = ${userId}`;
        
        console.log(`Executing query: ${query}`);
        
        // Simulated query execution
        setTimeout(() => {
            const result = { id: userId, name: 'Test User' };
            callback(null, result);
        }, 50);
    }
    
    // Improper error handling
    insertUser(userData) {
        try {
            // Missing validation
            const query = `INSERT INTO users (name, email) VALUES ('${userData.name}', '${userData.email}')`;
            
            // Potential XSS if data is not sanitized
            console.log(query);
            
            return { success: true };
        } catch (error) {
            // Exposing sensitive error information
            console.log(`Database error: ${error.stack}`);
            throw error;
        }
    }
    
    // Memory leak - event listeners not cleaned up
    setupEventListeners() {
        process.on('data', (data) => {
            // Memory leak: listener never removed
            this.processData(data);
        });
        
        // Multiple listeners for same event
        process.on('data', (data) => {
            this.logData(data);
        });
    }
}

class FileManager {
    constructor(basePath) {
        this.basePath = basePath;
    }
    
    // Path traversal vulnerability
    readFile(filename) {
        // No path sanitization
        const filePath = path.join(this.basePath, filename);
        
        try {
            // Synchronous file operations - blocking
            const content = fs.readFileSync(filePath, 'utf8');
            return content;
        } catch (error) {
            console.error('File read error:', error);
            return null;
        }
    }
    
    // Race condition potential
    writeFile(filename, content) {
        const filePath = path.join(this.basePath, filename);
        
        // Check if file exists
        if (fs.existsSync(filePath)) {
            // Race condition: file could be deleted between check and write
            console.log('File exists, overwriting...');
        }
        
        // No atomic write operation
        fs.writeFileSync(filePath, content);
    }
    
    // Inefficient directory listing
    listFiles() {
        const files = [];
        
        // Synchronous operation - blocks event loop
        const items = fs.readdirSync(this.basePath);
        
        for (const item of items) {
            const itemPath = path.join(this.basePath, item);
            
            // Multiple sync calls - very inefficient
            const stats = fs.statSync(itemPath);
            
            if (stats.isFile()) {
                files.push({
                    name: item,
                    size: stats.size,
                    modified: stats.mtime
                });
            }
        }
        
        return files;
    }
}

class ApiClient {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
        
        // Using deprecated request library
        this.requestDefaults = {
            timeout: 30000,
            rejectUnauthorized: false // Insecure SSL
        };
    }
    
    // Callback hell and poor error handling
    fetchUser(userId, callback) {
        const url = `${this.baseUrl}/users/${userId}`;
        
        request.get(url, this.requestDefaults, (error, response, body) => {
            if (error) {
                callback(error);
                return;
            }
            
            if (response.statusCode !== 200) {
                callback(new Error(`HTTP ${response.statusCode}`));
                return;
            }
            
            try {
                const data = JSON.parse(body);
                
                // Nested API call - callback hell
                this.fetchUserDetails(data.detailsUrl, (detailError, details) => {
                    if (detailError) {
                        callback(detailError);
                        return;
                    }
                    
                    const combined = { ...data, details };
                    callback(null, combined);
                });
                
            } catch (parseError) {
                callback(parseError);
            }
        });
    }
    
    fetchUserDetails(url, callback) {
        request.get(url, this.requestDefaults, (error, response, body) => {
            if (error) {
                callback(error);
                return;
            }
            
            try {
                const details = JSON.parse(body);
                callback(null, details);
            } catch (parseError) {
                callback(parseError);
            }
        });
    }
}

// Global variables - bad practice
var globalConfig = {
    environment: 'production', // Hardcoded environment
    debugMode: true, // Debug mode in production
    apiKey: 'secret-api-key-123' // Hardcoded API key
};

// Prototype pollution vulnerability
function mergeConfig(target, source) {
    for (let key in source) {
        // No hasOwnProperty check - prototype pollution risk
        target[key] = source[key];
    }
    return target;
}

// Improper input validation
function validateEmail(email) {
    // Weak regex that allows many invalid emails
    const regex = /.+@.+/;
    return regex.test(email);
}

// Missing error boundaries
function processUserData(userData) {
    // No null/undefined checks
    const name = userData.name.toLowerCase();
    const email = userData.email.trim();
    
    // Potential issues if userData properties are missing
    return {
        name: name,
        email: email,
        isValid: validateEmail(email)
    };
}

// Unhandled promise rejection
async function fetchExternalApi() {
    // No try-catch block
    const response = await fetch('https://api.external.com/data');
    const data = await response.json(); // Could fail if response is not JSON
    
    return data;
}

// Memory leak with timers
function startPeriodicTask() {
    // Timer never cleared
    setInterval(() => {
        console.log('Periodic task running...');
        
        // Potential memory leak: growing array
        globalData.push(new Date());
    }, 1000);
}

var globalData = []; // Global variable that grows indefinitely

// Usage that will cause issues
const dbManager = new DatabaseManager('mysql://localhost/test');
const fileManager = new FileManager('/tmp');

// This will cause issues due to hardcoded credentials and SQL injection risks
dbManager.queryUser("1; DROP TABLE users; --", (err, result) => {
    console.log('Query result:', result);
});

// Start memory leak
startPeriodicTask();

module.exports = {
    DatabaseManager,
    FileManager,
    ApiClient,
    mergeConfig,
    validateEmail,
    processUserData
};
