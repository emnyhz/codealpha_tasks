# Task 4 - Network Intrusion Detection System



## Overview



This project implements a Network Intrusion Detection System (NIDS) using Suricata on an Ubuntu AWS EC2 instance.



The system monitors network traffic, analyzes packets using Suricata detection rules, generates alerts for suspicious activity, records structured events in JSON format, and uses a custom response script to process security alerts.



## Environment



\- Platform: AWS EC2

\- Operating System: Ubuntu Linux

\- NIDS: Suricata 7.0.3

\- Network Interface: `ens5`

\- Rule Source: Emerging Threats Open

\- Log Analysis Tool: `jq`

\- Primary Logs:

&#x20; - `/var/log/suricata/fast.log`

&#x20; - `/var/log/suricata/eve.json`



## NIDS Architecture



```text

Internet / Test Client

&#x20;       |

&#x20;       v

AWS EC2 Network Interface (ens5)

&#x20;       |

&#x20;       v

&#x20;    Suricata

&#x20;       |

&#x20;       +----------------------+

&#x20;       |                      |

&#x20;       v                      v

&#x20;Emerging Threats         Custom Rules

&#x20;     Rules                local.rules

&#x20;       |                      |

&#x20;       +----------+-----------+

&#x20;                  |

&#x20;                  v

&#x20;             Alert Engine

&#x20;                  |

&#x20;        +---------+---------+

&#x20;        |                   |

&#x20;        v                   v

&#x20;    fast.log             eve.json

&#x20;                            |

&#x20;                            v

&#x20;                  Custom Response Script

&#x20;                            |

&#x20;                  +---------+---------+

&#x20;                  |                   |

&#x20;                  v                   v

&#x20;             Incident Log     Candidate Blocklist

```



## Suricata Configuration



During the initial setup, Suricata attempted to monitor the default `eth0` interface.



The AWS EC2 instance uses the `ens5` network interface, so the Suricata configuration was updated to monitor the correct interface.



The configuration was validated using:



```bash

sudo suricata -T -c /etc/suricata/suricata.yaml

```



After validation, the Suricata service was restarted and confirmed to be running successfully.



## Detection Rules



The project uses both Emerging Threats rules and custom Suricata rules.



The custom rules are stored in:



```text

rules/local.rules

```



### Custom Rules



| SID | Rule | Purpose | Validation |

|---|---|---|---|

| 1000001 | ICMP Echo Request Detection | Detect ICMP echo request traffic | Tested |

| 1000002 | Repeated SSH Connection Attempts | Detect repeated TCP SYN connections to SSH port 22 | Tested |

| 1000003 | Possible TCP SYN Port Scan | Detect high-rate TCP SYN activity | Tested |

| 1000004 | Suspicious `.env` File Access | Detect HTTP requests attempting to access `.env` files | Configured, not test-triggered |



## Rule 1000001 - ICMP Detection



The first custom rule detects ICMP Echo Request traffic.



Test traffic was generated using:



```bash

ping -c 4 8.8.8.8

```



Suricata successfully generated alerts with the signature:



```text

CODEALPHA ICMP Echo Request Detected

SID: 1000001

```



The generated alert included information such as:



\- Timestamp

\- Source IP

\- Destination IP

\- Protocol

\- Signature

\- Severity



The alert was visible in both `fast.log` and `eve.json`.



## Rule 1000002 - Repeated SSH Connection Attempts



A second custom rule was created to detect repeated TCP SYN connections to SSH port 22.



Controlled connection attempts were generated from a test client to the AWS EC2 instance.



Suricata successfully generated:



```text

CODEALPHA Repeated SSH Connection Attempts

SID: 1000002

Priority: 1

```



The same controlled traffic was also detected by an Emerging Threats rule as:



```text

ET SCAN Potential SSH Scan

```



This demonstrated that both the custom rule and the installed threat-detection rule set were analyzing the network traffic.



## Rule 1000003 - High-Rate TCP SYN Activity



A third custom rule was configured to detect a high number of TCP SYN packets from the same source within a short time period.



Controlled TCP connection traffic was generated during testing.



Suricata successfully generated:



```text

CODEALPHA Possible TCP SYN Port Scan

SID: 1000003

Priority: 2

```



This rule is used as an indicator of possible TCP SYN scanning or other unusually high-rate SYN activity.



## Rule 1000004 - Suspicious .env Access



A fourth custom rule was configured to detect HTTP requests attempting to access a `.env` file.



Such files may contain sensitive configuration information if accidentally exposed by a web application.



The rule was successfully added to the Suricata configuration, but a dedicated validation test was not performed for this rule.



## Real-Time Monitoring



Suricata continuously monitored traffic passing through the EC2 instance network interface.



Real-time JSON alerts were monitored using:



```bash

sudo tail -F /var/log/suricata/eve.json | jq --unbuffered '

select(.event\_type=="alert") |

{

&#x20; timestamp,

&#x20; src\_ip,

&#x20; src\_port,

&#x20; dest\_ip,

&#x20; dest\_port,

&#x20; proto,

&#x20; signature: .alert.signature,

&#x20; severity: .alert.severity

}'

```



This allowed alerts to be viewed immediately as matching network traffic was detected.



## EVE JSON Analysis



Suricata's `eve.json` log was used for structured alert analysis.



Custom ICMP alerts were filtered using `jq` and displayed with:



\- Timestamp

\- Source IP

\- Destination IP

\- Protocol

\- Signature

\- Severity



A copy of the extracted custom alert data is included in:



```text

reports/custom\_alerts.json

```



## Response Mechanism



A custom Bash response script was implemented:



```text

scripts/ids\_response.sh

```



The script reads Suricata alerts from:



```text

/var/log/suricata/eve.json

```



The response logic is:



```text

Severity 3

&#x20;   -> Log alert for monitoring



Severity 1 or 2

&#x20;   -> Log alert

&#x20;   -> Flag the source IP

&#x20;   -> Add the source IP to the candidate blocklist

```



The script generates:



```text

reports/incident\_response.log

reports/candidate\_blocklist.txt

```



Automatic firewall blocking was intentionally not enabled. This avoids accidentally blocking legitimate administrative traffic such as SSH.



The candidate blocklist therefore represents addresses requiring further investigation and should not automatically be treated as confirmed malicious hosts.



## Real-World Alert Detection



In addition to the controlled custom-rule tests, Suricata generated alerts from the Emerging Threats rule set for inbound traffic observed by the EC2 instance.



Examples included:



```text

ET DROP Spamhaus DROP Listed Traffic Inbound

ET DROP Dshield Block Listed Source

ET CINS Active Threat Intelligence Poor Reputation IP

ET SCAN Potential SSH Scan

```



These alerts demonstrate that the NIDS was actively processing real network traffic in addition to the controlled test traffic.



## Reports



The following evidence and report files are included:



```text

reports/

â”œâ”€â”€ candidate\_blocklist.txt

â”œâ”€â”€ custom\_alerts.json

â”œâ”€â”€ detection\_alerts.txt

â”œâ”€â”€ incident\_response.log

â”œâ”€â”€ suricata\_service\_status.txt

â””â”€â”€ suricata\_version.txt

```



### Report Description



\- `candidate\_blocklist.txt` - Source IP addresses flagged for further investigation.

\- `custom\_alerts.json` - Structured JSON output for custom Suricata alerts.

\- `detection\_alerts.txt` - Selected Suricata detection events.

\- `incident\_response.log` - Alerts processed by the response script.

\- `suricata\_service\_status.txt` - Suricata service status evidence.

\- `suricata\_version.txt` - Suricata version and build information.



## Project Structure



```text

Task4\_Network\_Intrusion\_Detection\_System/

â”‚

â”œâ”€â”€ reports/

â”‚   â”œâ”€â”€ candidate\_blocklist.txt

â”‚   â”œâ”€â”€ custom\_alerts.json

â”‚   â”œâ”€â”€ detection\_alerts.txt

â”‚   â”œâ”€â”€ incident\_response.log

â”‚   â”œâ”€â”€ suricata\_service\_status.txt

â”‚   â””â”€â”€ suricata\_version.txt

â”‚

â”œâ”€â”€ rules/

â”‚   â””â”€â”€ local.rules

â”‚

â”œâ”€â”€ scripts/

â”‚   â””â”€â”€ ids\_response.sh

â”‚

â”œâ”€â”€ screenshots/

â”‚   â””â”€â”€ Project implementation evidence

â”‚

â””â”€â”€ README.md

```



## Project Evidence



### 1. Suricata Installation



!\[Suricata Installation](screenshots/01\_suricata\_installation.png)



### 2. Initial Suricata Service Failure



!\[Initial Service Failure](screenshots/02\_suricata\_initial\_service\_failure.png)



The initial service issue helped identify that the default interface configuration did not match the AWS EC2 network interface.



### 3. Suricata Rules Update



!\[Rules Update](screenshots/03\_suricata\_rules\_update.png)



### 4. Suricata Service Running



!\[Suricata Running](screenshots/04\_suricata\_service\_running.png)



### 5. HOME\_NET and Local Rule Setup



!\[HOME NET Setup](screenshots/05\_home\_net\_and\_local\_rule\_setup.png)



### 6. Custom ICMP Rule Creation



!\[ICMP Rule](screenshots/06\_custom\_icmp\_rule\_creation.png)



### 7. Suricata Configuration Edit



!\[Configuration Edit](screenshots/07\_suricata\_configuration\_edit.png)



### 8. Local Rules Enabled



!\[Local Rules Enabled](screenshots/08\_local\_rules\_enabled\_in\_config.png)



### 9. Suricata Configuration Validation



!\[Configuration Test](screenshots/09\_suricata\_configuration\_test.png)



### 10. ICMP Test Traffic



!\[ICMP Test](screenshots/10\_icmp\_test\_traffic.png)



### 11. ICMP Alert Detection



!\[ICMP Alert](screenshots/11\_icmp\_alert\_detected.png)



### 12. EVE JSON Alert Analysis



!\[EVE JSON Analysis](screenshots/12\_eve\_json\_alert\_analysis.png)



### 13. Real-Time Alert Monitoring Setup



!\[Monitoring Setup](screenshots/13\_realtime\_alert\_monitoring\_setup.png)



### 14. Real-Time ICMP Test



!\[Real-Time ICMP](screenshots/14\_realtime\_icmp\_test.png)



### 15. Real-Time Suricata Alerts



!\[Real-Time Alerts](screenshots/15\_realtime\_suricata\_alerts.png)



### 16. Response Script Setup



!\[Response Setup](screenshots/16\_response\_script\_setup.png)



### 17. Response Script Code



!\[Response Script](screenshots/17\_response\_script\_code.png)



### 18. Response Script Permissions



!\[Script Permissions](screenshots/18\_response\_script\_permissions.png)



### 19. Response Script Execution



!\[Script Execution](screenshots/19\_response\_script\_execution.png)



### 20. Incident Response Results



!\[Incident Response](screenshots/20\_incident\_response\_results.png)



### 21. Candidate Blocklist Results



!\[Candidate Blocklist](screenshots/21\_candidate\_blocklist\_results.png)



### 22. Additional Custom Detection Rules



!\[Additional Rules](screenshots/22\_additional\_custom\_detection\_rules.png)



### 23. Rule Validation and Suricata Service



!\[Rule Validation](screenshots/23\_custom\_rules\_validation\_and\_service.png)



### 24. Controlled Repeated SSH Test



!\[SSH Test](screenshots/24\_repeated\_ssh\_test\_execution.png)



### 25. Repeated SSH Alert Detection



!\[SSH Alert](screenshots/25\_repeated\_ssh\_alert\_detected.png)



### 26. Controlled TCP SYN Test



!\[TCP SYN Test](screenshots/26\_tcp\_syn\_test\_execution.png)



### 27. High-Volume Connection Alert Evidence



!\[High Volume Alerts](screenshots/27\_high\_volume\_ssh\_alerts.png)



## Results



The project successfully demonstrated:



\- Suricata installation and configuration

\- AWS EC2 network interface monitoring

\- Emerging Threats rule integration

\- Custom Suricata detection rules

\- ICMP traffic detection

\- Repeated SSH connection detection

\- High-rate TCP SYN activity detection

\- Real-time network alert monitoring

\- Structured EVE JSON analysis

\- Incident logging

\- Candidate blocklist generation

\- Automated alert-response processing

\- Detection of live inbound network activity



## Security Considerations



No credentials, private keys, or AWS access keys are included in this repository.



The response mechanism does not automatically block detected IP addresses. Higher-priority alerts are flagged for investigation to reduce the risk of blocking legitimate traffic.



## Conclusion



This project demonstrates the deployment and operation of a Suricata-based Network Intrusion Detection System in a cloud environment.



The NIDS successfully monitored network traffic, detected controlled suspicious activity using custom rules, generated real-time alerts, processed structured security events, and implemented a basic incident-response workflow.



## Author



\*\*Emin Yahyazade\*\*



CodeAlpha Cyber Security Internship  

Task 4 - Network Intrusion Detection System


