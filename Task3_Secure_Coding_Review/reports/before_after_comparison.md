\# Secure Coding Review - Before and After Comparison



\## Project



CodeAlpha Cyber Security Internship - Task 3  

Language: Python  

Application: Flask Demo Application  

Static Analysis Tool: Bandit 1.9.4



\## Security Scan Comparison



| Metric | Vulnerable Version | Secure Version |

|---|---:|---:|

| High Severity Issues | 3 | 0 |

| Medium Severity Issues | 2 | 0 |

| Low Severity Issues | 2 | 0 |

| Total Issues | 7 | 0 |



\## Remediation Summary



\### 1. Hardcoded Secret Key



\*\*Before:\*\*  

The Flask secret key was stored directly in the source code.



\*\*After:\*\*  

The application loads the secret from the `FLASK\_SECRET\_KEY` environment variable and generates a secure temporary value when necessary.



\---



\### 2. Weak MD5 Hash



\*\*Before:\*\*  

The application used MD5, which is considered cryptographically weak.



\*\*After:\*\*  

MD5 was replaced with SHA-256 for the demonstration hashing functionality.



\---



\### 3. Unsafe eval()



\*\*Before:\*\*  

User-controlled expressions were passed directly to `eval()`.



\*\*After:\*\*  

`eval()` was completely removed and replaced with a restricted AST-based arithmetic parser.



\---



\### 4. SQL Injection



\*\*Before:\*\*  

SQL queries were built using user-controlled string interpolation.



\*\*After:\*\*  

Parameterized SQL queries are used with placeholders and separate query parameters.



\---



\### 5. Command Injection Risk



\*\*Before:\*\*  

User input was inserted into an operating system command executed with `shell=True`.



\*\*After:\*\*  

Operating system command execution was removed. IP addresses are now validated with Python's `ipaddress` module.



\---



\### 6. Flask Debug Mode



\*\*Before:\*\*  

The application was started with `debug=True`.



\*\*After:\*\*  

Debug mode was disabled.



\---



\### 7. Input Validation



\*\*Before:\*\*  

Multiple routes accepted user-controlled input without sufficient validation.



\*\*After:\*\*  

Length checks, type restrictions, safe parsing, and IP address validation were introduced.



\## Static Analysis Result



The original vulnerable application produced seven findings during the Bandit scan.



After remediation, Bandit reported:



`No issues identified.`



The secure version produced:



\- High Severity: 0

\- Medium Severity: 0

\- Low Severity: 0

\- Total Issues: 0



\## Conclusion



The secure coding review demonstrated how static analysis and manual inspection can identify insecure coding practices in a Python Flask application.



The identified issues were remediated by removing unsafe functionality, validating user input, parameterizing database queries, improving secret handling, replacing weak cryptographic functions, and disabling development debugging features.



A second Bandit scan confirmed that the issues identified by the static analyzer were no longer present in the remediated version.

