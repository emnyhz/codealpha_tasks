\# CodeAlpha Task 3 - Secure Coding Review



This project was created as part of the CodeAlpha Cyber Security Internship - Task 3.



\## Project Objective



The objective of this project is to review a Python Flask application for security vulnerabilities, identify insecure coding practices, apply remediation measures, and verify the improvements using static analysis.



\## Technologies Used



\- Python 3.13.15

\- Flask 3.1.3

\- Bandit 1.9.4

\- SQLite

\- Manual Code Review



\## Project Structure



\- `vulnerable\_app/` - intentionally vulnerable Flask application

\- `secure\_app/` - remediated secure version

\- `reports/` - Bandit scan reports and security findings

\- `requirements.txt` - project dependencies

\- `.gitignore` - excluded local and sensitive files



\## Vulnerabilities Identified



The original application contained several insecure coding practices:



\- Hardcoded secret key

\- Weak MD5 hashing

\- Unsafe use of `eval()`

\- SQL injection risk

\- Operating system command execution with `shell=True`

\- Unvalidated user input

\- Flask debug mode enabled



\## Static Analysis Results



\### Vulnerable Version



Bandit identified:



\- High Severity: 3

\- Medium Severity: 2

\- Low Severity: 2

\- Total Issues: 7



\### Secure Version



After remediation, Bandit reported:



\- High Severity: 0

\- Medium Severity: 0

\- Low Severity: 0

\- Total Issues: 0



Bandit result:



`No issues identified.`



\## Remediation Measures



The following security improvements were implemented:



\- Removed unsafe `eval()` usage

\- Replaced MD5 with SHA-256

\- Implemented parameterized SQL queries

\- Removed `shell=True` command execution

\- Added user input validation

\- Added IP address validation

\- Moved secret handling away from hardcoded source values

\- Disabled Flask debug mode

\- Added safer error handling



\## Reports



The `reports` directory contains:



\- `bandit\_vulnerable\_report.txt`

\- `bandit\_secure\_report.txt`

\- `security\_findings.md`

\- `before\_after\_comparison.md`



\## Security Review Result



The project demonstrates a complete secure coding review workflow:



Vulnerable Application → Static Analysis → Manual Review → Remediation → Re-scan → Comparison



The second Bandit scan confirmed that the issues detected by the static analyzer were no longer present in the remediated application.



\## Author



Emin Yahyazadə



\## Internship



CodeAlpha Cyber Security Internship - Task 3

