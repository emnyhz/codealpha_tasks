#!/bin/bash

EVE="/var/log/suricata/eve.json"
INCIDENT_LOG="$HOME/codealpha-task4/reports/incident_response.log"
BLOCKLIST="$HOME/codealpha-task4/reports/candidate_blocklist.txt"

echo "=== CodeAlpha IDS Response ==="
echo "Analyzing Suricata alerts..."

sudo jq -r '
select(.event_type=="alert") |
[
  .timestamp,
  .src_ip,
  .dest_ip,
  .proto,
  .alert.signature,
  .alert.severity
] | @tsv
' "$EVE" | tail -n 20 |
while IFS=$'\t' read -r timestamp src_ip dest_ip proto signature severity
do
    echo "$timestamp | $src_ip -> $dest_ip | $proto | Severity $severity | $signature" \
        >> "$INCIDENT_LOG"

    if [ "$severity" -le 2 ]; then
        echo "$src_ip" >> "$BLOCKLIST"
        echo "[RESPONSE] High-priority source flagged: $src_ip"
    else
        echo "[MONITOR] Alert logged: $signature"
    fi
done

sort -u "$BLOCKLIST" -o "$BLOCKLIST" 2>/dev/null || true

echo
echo "Incident log: $INCIDENT_LOG"
echo "Candidate blocklist: $BLOCKLIST"
