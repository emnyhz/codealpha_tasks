\# Secure Coding Review - Security Findings



\## Project



CodeAlpha Cyber Security Internship - Task 3  

Application: Python Flask Demo Application  

Static Analyzer: Bandit 1.9.4  

Review Method: Static Analysis + Manual Code Review



\## Scan Summary



Bandit identified 7 security issues in the vulnerable application:



\- High Severity: 3

\- Medium Severity: 2

\- Low Severity: 2



\## Findings



| ID | Vulnerability | Severity | Risk | Recommended Remediation |

|---|---|---|---|---|

| B404 | Use of subprocess module | Low | Executing operating system commands can introduce command execution risks if input is not controlled. | Avoid unnecessary OS command execution and use safer Python libraries where possible. |

| B105 | Hardcoded Secret Key | Low | Secrets stored directly in source code can be exposed through repositories or source leaks. | Load secret values from environment variables or a secure secret manager. |

| B324 | Weak MD5 Hash | High | MD5 is cryptographically weak and should not be used for security-sensitive hashing. | Replace MD5 with a secure algorithm such as SHA-256 for integrity use cases or a password hashing function for passwords. |

| B307 | Unsafe eval() | Medium | eval() can execute arbitrary Python code supplied by an attacker. | Remove eval() and implement strict input validation or safe parsing. |

| B608 | SQL Injection | Medium | Building SQL queries with user-controlled strings can allow attackers to modify database queries. | Use parameterized SQL queries instead of string formatting. |

| B602 | shell=True Command Execution | High | User input passed to a shell command may allow operating system command injection. | Avoid shell=True and pass validated arguments as a list to subprocess functions. |

| B201 | Flask Debug Mode Enabled | High | Debug mode may expose the Werkzeug debugger and sensitive application information. | Disable debug mode in production environments. |



\## Manual Review Notes



Manual inspection confirmed that several vulnerabilities originate from untrusted user input being used directly in dangerous operations.



The following security problems were confirmed:



1\. User-controlled data reaches eval() without validation.

2\. SQL queries are constructed using string interpolation.

3\. User-controlled host values are included in operating system commands.

4\. A secret key is stored directly in source code.

5\. The application runs with Flask debug mode enabled.

6\. MD5 is used as a weak cryptographic hash.



\## Remediation Plan



A secure version of the application will be created with the following changes:



\- Remove eval().

\- Replace MD5 with SHA-256.

\- Use parameterized SQL queries.

\- Validate user input.

\- Remove shell=True from subprocess execution.

\- Store the Flask secret key in an environment variable.

\- Disable Flask debug mode.

\- Add safe error handling.



\## Conclusion



The static analysis and manual review identified multiple insecure coding practices in the original application. The next stage of the project will implement remediation measures and re-scan the secure version to verify that the identified vulnerabilities have been reduced or eliminated.

