# Network Intrusion Detection System Report



## CodeAlpha Cyber Security Internship - Task 4



**Author:** Emin Yahyazade  

**Project:** Network Intrusion Detection System  

**Platform:** AWS EC2 Ubuntu Linux  

**NIDS:** Suricata 7.0.3  

**Date:** September 2026



\---



## 1. Executive Summary



This project implements a Network Intrusion Detection System (NIDS) using Suricata on an Ubuntu-based AWS EC2 instance.



The objective was to deploy an intrusion detection solution capable of continuously monitoring network traffic, applying both standard and custom detection rules, generating alerts for suspicious activity, analyzing structured security events, and implementing a basic response mechanism.



The implementation successfully detected controlled ICMP traffic, repeated SSH connection attempts, and high-rate TCP SYN activity. Suricata also generated alerts from the Emerging Threats rule set for inbound traffic observed on the EC2 instance.



A custom Bash response script was developed to process Suricata alerts, record incident information, and identify higher-priority source IP addresses for further investigation.



\---



## 2. Project Objectives



The main objectives of the project were:



\- Install and configure a Network Intrusion Detection System.

\- Monitor network traffic continuously.

\- Configure Suricata detection rules.

\- Create custom detection rules.

\- Generate controlled traffic to validate detection.

\- Analyze alerts using `fast.log` and `eve.json`.

\- Implement a basic incident-response mechanism.

\- Maintain evidence of detected events and response actions.



\---



## 3. Environment



The NIDS was deployed using the following environment:



| Component | Configuration |

|---|---|

| Cloud Platform | AWS EC2 |

| Operating System | Ubuntu Linux |

| IDS Software | Suricata 7.0.3 |

| Network Interface | ens5 |

| Rule Set | Emerging Threats Open |

| JSON Processing | jq |

| Alert Log | `/var/log/suricata/fast.log` |

| Structured Event Log | `/var/log/suricata/eve.json` |



\---



## 4. Suricata Installation and Configuration



Suricata and `jq` were installed on the Ubuntu EC2 instance.



The initial Suricata service configuration expected an interface named:



```text

eth0

```



However, the AWS EC2 instance used:



```text

ens5

```



This resulted in an initial service failure.



The Suricata configuration was updated so that the AF-Packet capture configuration used the correct AWS interface.



The configuration was then validated using:



```bash

sudo suricata -T -c /etc/suricata/suricata.yaml

```



After the configuration was corrected, Suricata successfully started and continuously monitored traffic through the `ens5` interface.



\---



## 5. Detection Rule Configuration



Suricata was configured to use the Emerging Threats rule set together with a custom rule file:



```text

/var/lib/suricata/rules/local.rules

```



The project copy of the custom rules is stored in:



```text

rules/local.rules

```



Four custom detection rules were created.



### Rule 1000001 - ICMP Echo Request Detection



Purpose:



Detect ICMP Echo Request traffic originating from the monitored network.



Signature:



```text

CODEALPHA ICMP Echo Request Detected

```



Status:



```text

Successfully tested

```



\---



### Rule 1000002 - Repeated SSH Connection Attempts



Purpose:



Detect multiple TCP SYN connection attempts from the same source toward SSH port 22.



Detection threshold:



```text

5 connections within 60 seconds

```



Signature:



```text

CODEALPHA Repeated SSH Connection Attempts

```



Priority:



```text

1

```



Status:



```text

Successfully tested

```



\---



### Rule 1000003 - High-Rate TCP SYN Activity



Purpose:



Detect a high rate of TCP SYN packets from the same source within a short period.



Detection threshold:



```text

20 SYN packets within 10 seconds

```



Signature:



```text

CODEALPHA Possible TCP SYN Port Scan

```



Priority:



```text

2

```



Status:



```text

Successfully tested

```



The rule is used as an indication of possible scanning or unusually high-rate TCP SYN activity.



\---



### Rule 1000004 - Suspicious .env File Access



Purpose:



Detect HTTP requests attempting to access a `.env` resource.



Signature:



```text

CODEALPHA Suspicious .env File Access Attempt

```



Priority:



```text

1

```



Status:



```text

Configured but not test-triggered

```



This rule was included because `.env` files may contain sensitive application configuration information if incorrectly exposed by a web server.



\---



## 6. ICMP Detection Test



Controlled ICMP traffic was generated from the EC2 server using:



```bash

ping -c 4 8.8.8.8

```



Suricata detected the ICMP Echo Requests and generated alerts using custom SID:



```text

1000001

```



Example detection:



```text

CODEALPHA ICMP Echo Request Detected

```



The alerts contained:



\- Source IP

\- Destination IP

\- Protocol

\- Timestamp

\- Detection signature

\- Severity



The same alerts were visible in both `fast.log` and `eve.json`.



### Result



```text

ICMP Detection: PASS

```



\---



## 7. EVE JSON Alert Analysis



Suricata records structured event data inside:



```text

/var/log/suricata/eve.json

```



The custom ICMP alerts were filtered using `jq`.



The extracted information included:



```text

timestamp

src_ip

dest_ip

proto

signature

severity

```



The JSON analysis confirmed that the custom detection rule was being processed correctly by Suricata.



A project copy of the extracted custom alerts is stored in:



```text

reports/custom_alerts.json

```



\---



## 8. Continuous Network Monitoring



Real-time alert monitoring was implemented using Suricata's EVE JSON output.



The monitoring command used was:



```bash

sudo tail -F /var/log/suricata/eve.json | jq --unbuffered '

select(.event_type=="alert") |

{

&#x20; timestamp,

&#x20; src_ip,

&#x20; src_port,

&#x20; dest_ip,

&#x20; dest_port,

&#x20; proto,

&#x20; signature: .alert.signature,

&#x20; severity: .alert.severity

}'

```



While this command was running, controlled ICMP traffic was generated.



Suricata immediately displayed matching alerts in real time.



### Result



```text

Continuous Monitoring: PASS

```



This demonstrated that the IDS was actively monitoring the EC2 network interface and processing new traffic as it arrived.



\---



## 9. Repeated SSH Connection Detection



Controlled TCP connection attempts were generated from an external test client toward SSH port 22 of the AWS EC2 instance.



The custom rule successfully generated:



```text

CODEALPHA Repeated SSH Connection Attempts

SID: 1000002

Priority: 1

```



During the same controlled traffic test, an Emerging Threats rule also generated:



```text

ET SCAN Potential SSH Scan

```



This provided additional evidence that both the custom detection logic and the installed threat detection rules were analyzing the same network traffic.



### Result



```text

Repeated SSH Detection: PASS

```



\---



## 10. TCP SYN Activity Detection



A larger number of controlled TCP connection attempts were generated to test the high-rate SYN detection rule.



The custom rule successfully generated:



```text

CODEALPHA Possible TCP SYN Port Scan

SID: 1000003

Priority: 2

```



The test demonstrated that Suricata could identify a high number of TCP SYN packets from the same source in a short period.



### Result



```text

High-Rate TCP SYN Detection: PASS

```



\---



## 11. Emerging Threats Detection



In addition to the controlled tests, Suricata generated alerts using the installed Emerging Threats rules.



Examples observed included:



```text

ET DROP Spamhaus DROP Listed Traffic Inbound

```



```text

ET DROP Dshield Block Listed Source

```



```text

ET CINS Active Threat Intelligence Poor Reputation IP

```



```text

ET SCAN Potential SSH Scan

```



These alerts showed that the NIDS was processing live inbound network activity in addition to the controlled custom-rule tests.



These events should be interpreted as detection-rule matches requiring investigation rather than automatic proof that every source was malicious.



\---



## 12. Incident Response Mechanism



A custom Bash script was developed:



```text

scripts/ids_response.sh

```



The script processes Suricata alerts from:



```text

/var/log/suricata/eve.json

```



The response workflow is:



```text

Suricata Alert

&#x20;     |

&#x20;     v

Read Alert Severity

&#x20;     |

&#x20;     +-------------------------+

&#x20;     |                         |

&#x20;     v                         v

Severity 3                 Severity 1 or 2

&#x20;     |                         |

&#x20;     v                         v

Log for Monitoring        Log Incident

&#x20;                               |

&#x20;                               v

&#x20;                        Flag Source IP

&#x20;                               |

&#x20;                               v

&#x20;                      Candidate Blocklist

```



The script creates:



```text

reports/incident_response.log

```



and:



```text

reports/candidate_blocklist.txt

```



Higher-priority source IP addresses are recorded for further investigation.



\---



## 13. Response Safety



The response mechanism does not automatically modify firewall rules.



Automatic IP blocking was intentionally avoided because an incorrectly classified source could include legitimate administrative traffic.



For example, automatically blocking a source IP during an SSH-related test could result in loss of remote management access.



The implemented approach therefore follows:



```text

Detect

&#x20;  â†“

Log

&#x20;  â†“

Flag

&#x20;  â†“

Investigate

&#x20;  â†“

Block manually if confirmed necessary

```



This provides a safer response workflow for the project environment.



\---



## 14. Incident Response Results



The response script successfully processed Suricata alerts.



Severity 3 custom ICMP alerts were logged for monitoring.



Higher-priority alerts were identified and their source IP addresses were added to:



```text

candidate_blocklist.txt

```



The candidate blocklist contains addresses that should be reviewed further.



An address appearing in the candidate blocklist is not automatically treated as a confirmed attacker.



\---



## 15. Detection Summary



| Detection | SID / Source | Result |

|---|---|---|

| ICMP Echo Request | 1000001 | PASS |

| Repeated SSH Connections | 1000002 | PASS |

| High-Rate TCP SYN Activity | 1000003 | PASS |

| Suspicious `.env` Access | 1000004 | Configured, not test-triggered |

| ET SSH Scan Detection | Emerging Threats | Detected |

| ET Reputation / Blocklist Alerts | Emerging Threats | Detected |

| Real-Time EVE Monitoring | Suricata | PASS |

| Response Script | Custom Bash Script | PASS |

| Candidate Blocklist | Response Mechanism | PASS |



\---



## 16. Evidence Files



The following report files were collected from the NIDS environment:



```text

reports/

â”œâ”€â”€ candidate_blocklist.txt

â”œâ”€â”€ custom_alerts.json

â”œâ”€â”€ detection_alerts.txt

â”œâ”€â”€ incident_response.log

â”œâ”€â”€ nids_report.md

â”œâ”€â”€ suricata_service_status.txt

â””â”€â”€ suricata_version.txt

```



### candidate_blocklist.txt



Contains higher-priority source IP addresses identified by the response script for further investigation.



### custom_alerts.json



Contains structured custom Suricata alert information extracted from `eve.json`.



### detection_alerts.txt



Contains selected custom and Emerging Threats alert evidence from `fast.log`.



### incident_response.log



Contains alert information processed by the custom response script.



### suricata_service_status.txt



Contains evidence of the Suricata service status.



### suricata_version.txt



Contains Suricata build and version information.



\---



## 17. Security Findings



### Finding 1 - Incorrect Default Network Interface



**Issue:**



Suricata initially attempted to monitor `eth0`, while the AWS EC2 instance used `ens5`.



**Impact:**



Suricata could not successfully initialize packet capture.



**Resolution:**



The AF-Packet configuration was updated to use:



```text

ens5

```



**Status:**



```text

Resolved

```



\---



### Finding 2 - Repeated SSH Connection Activity



**Issue:**



Multiple TCP SYN connections toward SSH can indicate scanning, automated connection attempts, or other suspicious behavior.



**Detection:**



```text

CODEALPHA Repeated SSH Connection Attempts

```



**Response:**



The event is logged and higher-priority sources can be flagged for further investigation.



**Status:**



```text

Successfully Detected

```



\---



### Finding 3 - High-Rate TCP SYN Activity



**Issue:**



A high number of SYN packets from a single source over a short period can indicate network scanning or abnormal connection activity.



**Detection:**



```text

CODEALPHA Possible TCP SYN Port Scan

```



**Response:**



The alert is recorded and may be reviewed as part of the incident-response workflow.



**Status:**



```text

Successfully Detected

```



\---



### Finding 4 - Sensitive File Access Pattern



**Issue:**



Requests for `.env` files may indicate attempts to discover sensitive application configuration.



**Detection Rule:**



```text

CODEALPHA Suspicious .env File Access Attempt

```



**Status:**



```text

Rule configured, dedicated validation test not performed

```



\---



## 18. Recommendations



The following improvements could be applied in a production environment:



\- Regularly update Suricata rule sets.

\- Review high-priority alerts before blocking source IP addresses.

\- Restrict SSH access to trusted IP addresses or VPN connections.

\- Use strong SSH authentication and disable password authentication where appropriate.

\- Centralize Suricata logs using a SIEM platform.

\- Add alert dashboards for faster investigation.

\- Configure alert notifications for critical events.

\- Tune custom detection thresholds to reduce false positives.

\- Periodically review `HOME_NET` and monitored interfaces.

\- Protect web applications against accidental exposure of sensitive files such as `.env`.

\- Use AWS VPC Traffic Mirroring if broader VPC-level traffic inspection is required.



\---



## 19. Limitations



The Suricata deployment monitors traffic visible to the EC2 instance network interface.



It does not automatically monitor all traffic across an entire AWS VPC.



Broader network visibility would require additional architecture such as AWS VPC Traffic Mirroring or deployment of Suricata at an appropriate network monitoring point.



The `.env` detection rule was configured but was not separately validation-tested during this project.



The response mechanism flags higher-priority sources for investigation but does not automatically enforce firewall blocks.



\---



## 20. Final Result



The project successfully met the primary Network Intrusion Detection System requirements.



The implementation demonstrated:



\- Suricata installation and configuration

\- AWS EC2 traffic monitoring

\- Emerging Threats integration

\- Custom detection rules

\- Controlled security testing

\- ICMP detection

\- Repeated SSH connection detection

\- High-rate TCP SYN activity detection

\- Continuous real-time monitoring

\- EVE JSON security event analysis

\- Incident logging

\- Candidate blocklist generation

\- Basic automated alert-response processing



The result is a functional Suricata-based NIDS capable of monitoring network traffic, identifying suspicious activity, generating security alerts, and supporting an incident-response workflow.



\---



## 21. Conclusion



This project provided practical experience in deploying and operating a Network Intrusion Detection System in a cloud environment.



Suricata successfully monitored traffic on the AWS EC2 instance, processed both Emerging Threats and custom detection rules, generated real-time alerts, and recorded structured security events.



The addition of a custom response script extended the project beyond detection by introducing alert processing, incident logging, and candidate source identification.



Overall, the project demonstrates the core workflow of:



```text

Monitor â†’ Detect â†’ Analyze â†’ Alert â†’ Respond

```



\---



**Emin Yahyazade**  

CodeAlpha Cyber Security Internship  

Task 4 - Network Intrusion Detection System


