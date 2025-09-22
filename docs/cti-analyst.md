# CTI Analyst Walkthrough

This guide explains the CTI Analyst tasks.

## Accessing the VM
1. Launch the **CTI Analyst** exercise in KYPO.
2. Connect to `soc-server` (`10.10.20.10`) as `ubuntu`.

## Steps
1. Open MISP in a browser on `soc-server` (`http://localhost/`).
   - Create a new event and add the hash of `malware.exe`.
   - Submit the event and note the assigned event ID for KYPO.
2. Search MISP for the domain `evil.example.com`.
   - Identify the related threat actor and record it in KYPO.

## Documenting Findings
Enter the event ID and threat actor name in the **CTI Analyst** exercise fields within KYPO.
