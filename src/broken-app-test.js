// Intentionally broken JavaScript file to trigger CI/CD failure
const app = require('express');  // Missing dependency
const missingModule = require('nonexistent-module');  // This will fail

// Syntax error below
function brokenFunction() {
    console.log("This function has syntax errors"
    // Missing closing parenthesis and semicolon
}

// Undefined variable usage
undefinedVariable.someMethod();

// Export statement
module.exports = app;
