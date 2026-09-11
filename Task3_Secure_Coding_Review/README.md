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


## Project Evidence

The following screenshots document the complete secure coding review process from environment setup to vulnerability detection, remediation, and final verification.

### 1. Project Structure
![Project Structure](screenshots/01_project_structure.png)

### 2. Environment Setup
![Environment Setup](screenshots/02_environment_setup.png)

### 3. Security Tools Installed and Verified
![Security Tools](screenshots/03_tools_installed_and_verified.png)

### 4. Vulnerable Application Creation
![Vulnerable App Creation](screenshots/04_vulnerable_app_creation.png)

### 5. Vulnerable Application Source Code
![Vulnerable Application](screenshots/05_vulnerable_app_code.png)

### 6. Bandit Scan of Vulnerable Application
![Bandit Vulnerable Scan](screenshots/06_bandit_vulnerable_scan.png)

### 7. Vulnerable Scan Report
![Vulnerable Scan Report](screenshots/07_vulnerable_scan_report.png)

### 8. Security Findings Creation
![Security Findings Creation](screenshots/08_security_findings_creation.png)

### 9. Security Findings and Manual Review
![Security Findings](screenshots/09_security_findings.png)

### 10. Secure Application Creation
![Secure App Creation](screenshots/10_secure_app_creation.png)

### 11. Remediated Secure Application
![Secure Application](screenshots/11_secure_app_code.png)

### 12. Bandit Re-scan of Secure Application
![Bandit Secure Scan](screenshots/12_bandit_secure_scan.png)

### 13. Secure Scan Report
![Secure Scan Report](screenshots/13_secure_scan_report.png)

### 14. Before/After Report Creation
![Comparison Report Creation](screenshots/14_before_after_report_creation.png)

### 15. Before and After Security Comparison
![Before After Comparison](screenshots/15_before_after_comparison.png)

### 16. Requirements File Creation
![Requirements Creation](screenshots/16_requirements_creation.png)

### 17. Project Dependencies
![Requirements](screenshots/17_requirements_content.png)

### 18. GitIgnore Creation
![GitIgnore Creation](screenshots/18_gitignore_creation.png)

### 19. GitIgnore Configuration
![GitIgnore](screenshots/19_gitignore_content.png)

### 20. README Creation
![README Creation](screenshots/20_readme_creation.png)

### 21. Project Documentation
![README](screenshots/21_readme_content.png)

### 22. Final Project Structure
![Final Structure](screenshots/22_final_project_structure.png)