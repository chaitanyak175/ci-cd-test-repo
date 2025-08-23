// Intentionally broken JavaScript file for testing
// Multiple syntax and logic errors

const express = require('express'); // Missing dependency
const missingModule = require('nonexistent-module'); // Will cause error

// Syntax error: missing closing bracket
function brokenFunction() {
    console.log("This function has syntax errors"
    return "missing semicolon and bracket"

// Undefined variable usage
function anotherBrokenFunction() {
    console.log(undefinedVariable); // ReferenceError
    return nonExistentFunction(); // TypeError
}

// Missing exports
module.exports = {
    brokenFunction,
    // Missing comma will cause syntax error
    anotherBrokenFunction
    missingComma: true
};
