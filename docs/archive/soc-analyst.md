# SOC Analyst Walkthrough

This guide explains how to complete the SOC Analyst exercise in KYPO.

## Accessing the VM
1. Start the **SOC Analyst** exercise in KYPO.
2. Open a terminal to `soc-server` (IP `10.10.20.10`) and log in as `ubuntu`.

## Steps
1. View recent alerts:
   ```bash
   sudo tail -n 5 /var/log/wazuh/alerts/alerts.json
   ```
   - Note the alert ID mentioning `user-pc` and record it in the first answer field.
2. Check for connections to the suspicious IP:
   ```bash
   netstat -tunap | grep 192.0.2.123
   ```
   - Record the process name in KYPO.
3. In a browser on `soc-server`, open TheHive (`http://localhost:9000`) and create a case named **Suspicious login**.
   - Leave the status as **Open** and add this status in the final answer field.

## Documenting Findings
Enter your answers directly into the KYPO web interface under the **SOC Analyst** exercise. Each question corresponds to one of the steps above.
