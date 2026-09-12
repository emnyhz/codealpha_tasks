# Task 4 - Network Intrusion Detection System

## Overview

This project implements a Network Intrusion Detection System (NIDS) using Suricata on an Ubuntu AWS EC2 instance.

The system monitors network traffic, analyzes packets using Suricata detection rules, generates alerts for suspicious activity, records structured events in JSON format, and uses a custom response script to process security alerts.

## Environment

- Platform: AWS EC2
- Operating System: Ubuntu Linux
- NIDS: Suricata 7.0.3
- Network Interface: `ens5`
- Rule Source: Emerging Threats Open
- Log Analysis Tool: `jq`
- Primary Logs:
  - `/var/log/suricata/fast.log`
  - `/var/log/suricata/eve.json`

## NIDS Architecture

```text
Internet / Test Client
        |
        v
AWS EC2 Network Interface (ens5)
        |
        v
     Suricata
        |
        +----------------------+
        |                      |
        v                      v
 Emerging Threats         Custom Rules
      Rules                local.rules
        |                      |
        +----------+-----------+
                   |
                   v
              Alert Engine
                   |
         +---------+---------+
         |                   |
         v                   v
     fast.log             eve.json
                             |
                             v
                   Custom Response Script
                             |
                   +---------+---------+
                   |                   |
                   v                   v
              Incident Log     Candidate Blocklist
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

- Timestamp
- Source IP
- Destination IP
- Protocol
- Signature
- Severity

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
select(.event_type=="alert") |
{
  timestamp,
  src_ip,
  src_port,
  dest_ip,
  dest_port,
  proto,
  signature: .alert.signature,
  severity: .alert.severity
}'
```

This allowed alerts to be viewed immediately as matching network traffic was detected.

## EVE JSON Analysis

Suricata's `eve.json` log was used for structured alert analysis.

Custom ICMP alerts were filtered using `jq` and displayed with:

- Timestamp
- Source IP
- Destination IP
- Protocol
- Signature
- Severity

A copy of the extracted custom alert data is included in:

```text
reports/custom_alerts.json
```

## Response Mechanism

A custom Bash response script was implemented:

```text
scripts/ids_response.sh
```

The script reads Suricata alerts from:

```text
/var/log/suricata/eve.json
```

The response logic is:

```text
Severity 3
    -> Log alert for monitoring

Severity 1 or 2
    -> Log alert
    -> Flag the source IP
    -> Add the source IP to the candidate blocklist
```

The script generates:

```text
reports/incident_response.log
reports/candidate_blocklist.txt
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
|-- candidate_blocklist.txt
|-- custom_alerts.json
|-- detection_alerts.txt
|-- incident_response.log
|-- nids_report.md
|-- suricata_service_status.txt
`-- suricata_version.txt
```

### Report Description

- `candidate_blocklist.txt` - Source IP addresses flagged for further investigation.
- `custom_alerts.json` - Structured JSON output for custom Suricata alerts.
- `detection_alerts.txt` - Selected Suricata detection events.
- `incident_response.log` - Alerts processed by the response script.
- `nids_report.md` - Detailed Network Intrusion Detection System project report.
- `suricata_service_status.txt` - Suricata service status evidence.
- `suricata_version.txt` - Suricata version and build information.

## Project Structure

```text
Task4_Network_Intrusion_Detection_System/
|
|-- reports/
|   |-- candidate_blocklist.txt
|   |-- custom_alerts.json
|   |-- detection_alerts.txt
|   |-- incident_response.log
|   |-- nids_report.md
|   |-- suricata_service_status.txt
|   `-- suricata_version.txt
|
|-- rules/
|   `-- local.rules
|
|-- scripts/
|   `-- ids_response.sh
|
|-- screenshots/
|   `-- Project implementation evidence
|
`-- README.md
```

## Project Evidence

### 1. Suricata Installation

![Suricata Installation](screenshots/01_suricata_installation.png)

### 2. Initial Suricata Service Failure

![Initial Service Failure](screenshots/02_suricata_initial_service_failure.png)

The initial service issue helped identify that the default interface configuration did not match the AWS EC2 network interface.

### 3. Suricata Rules Update

![Rules Update](screenshots/03_suricata_rules_update.png)

### 4. Suricata Service Running

![Suricata Running](screenshots/04_suricata_service_running.png)

### 5. HOME_NET and Local Rule Setup

![HOME NET Setup](screenshots/05_home_net_and_local_rule_setup.png)

### 6. Custom ICMP Rule Creation

![ICMP Rule](screenshots/06_custom_icmp_rule_creation.png)

### 7. Suricata Configuration Edit

![Configuration Edit](screenshots/07_suricata_configuration_edit.png)

### 8. Local Rules Enabled

![Local Rules Enabled](screenshots/08_local_rules_enabled_in_config.png)

### 9. Suricata Configuration Validation

![Configuration Test](screenshots/09_suricata_configuration_test.png)

### 10. ICMP Test Traffic

![ICMP Test](screenshots/10_icmp_test_traffic.png)

### 11. ICMP Alert Detection

![ICMP Alert](screenshots/11_icmp_alert_detected.png)

### 12. EVE JSON Alert Analysis

![EVE JSON Analysis](screenshots/12_eve_json_alert_analysis.png)

### 13. Real-Time Alert Monitoring Setup

![Monitoring Setup](screenshots/13_realtime_alert_monitoring_setup.png)

### 14. Real-Time ICMP Test

![Real-Time ICMP](screenshots/14_realtime_icmp_test.png)

### 15. Real-Time Suricata Alerts

![Real-Time Alerts](screenshots/15_realtime_suricata_alerts.png)

### 16. Response Script Setup

![Response Setup](screenshots/16_response_script_setup.png)

### 17. Response Script Code

![Response Script](screenshots/17_response_script_code.png)

### 18. Response Script Permissions

![Script Permissions](screenshots/18_response_script_permissions.png)

### 19. Response Script Execution

![Script Execution](screenshots/19_response_script_execution.png)

### 20. Incident Response Results

![Incident Response](screenshots/20_incident_response_results.png)

### 21. Candidate Blocklist Results

![Candidate Blocklist](screenshots/21_candidate_blocklist_results.png)

### 22. Additional Custom Detection Rules

![Additional Rules](screenshots/22_additional_custom_detection_rules.png)

### 23. Rule Validation and Suricata Service

![Rule Validation](screenshots/23_custom_rules_validation_and_service.png)

### 24. Controlled Repeated SSH Test

![SSH Test](screenshots/24_repeated_ssh_test_execution.png)

### 25. Repeated SSH Alert Detection

![SSH Alert](screenshots/25_repeated_ssh_alert_detected.png)

### 26. Controlled TCP SYN Test

![TCP SYN Test](screenshots/26_tcp_syn_test_execution.png)

### 27. High-Volume Connection Alert Evidence

![High Volume Alerts](screenshots/27_high_volume_ssh_alerts.png)

## Results

The project successfully demonstrated:

- Suricata installation and configuration
- AWS EC2 network interface monitoring
- Emerging Threats rule integration
- Custom Suricata detection rules
- ICMP traffic detection
- Repeated SSH connection detection
- High-rate TCP SYN activity detection
- Real-time network alert monitoring
- Structured EVE JSON analysis
- Incident logging
- Candidate blocklist generation
- Automated alert-response processing
- Detection of live inbound network activity

## Security Considerations

No credentials, private keys, or AWS access keys are included in this repository.

The response mechanism does not automatically block detected IP addresses. Higher-priority alerts are flagged for investigation to reduce the risk of blocking legitimate traffic.

## Conclusion

This project demonstrates the deployment and operation of a Suricata-based Network Intrusion Detection System in a cloud environment.

The NIDS successfully monitored network traffic, detected controlled suspicious activity using custom rules, generated real-time alerts, processed structured security events, and implemented a basic incident-response workflow.

## Author

**Emin Yahyazade**

CodeAlpha Cyber Security Internship  
Task 4 - Network Intrusion Detection System
