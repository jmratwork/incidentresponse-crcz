# Incident Responder Walkthrough

This guide covers the Incident Responder tasks.

## Accessing the VM
1. Start the **Incident Responder** exercise in KYPO.
2. Connect to `user-pc` (IP `10.10.10.50`) via the console or RDP using the `Administrator` account.

## Steps
1. Acquire a memory image:
   ```powershell
   winpmem_mini.exe -o C:\evidence\mem.raw
   ```
   - Record the full path of the image in KYPO.
2. Copy the suspicious executable from the temporary directory:
   - Browse to `C:\Users\User\AppData\Temp` and note the file name (e.g., `malware.exe`).
   - Provide the file name in KYPO.
3. Analyze the image on `soc-server` (SSH `ubuntu@soc-server`):
   ```bash
   volatility -f mem.raw pslist | grep malware
   ```
   - Enter the PID found in the last answer field.

## Documenting Findings
Provide each answer in the KYPO **Incident Responder** exercise as you complete the steps.
