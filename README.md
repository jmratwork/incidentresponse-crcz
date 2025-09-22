# Incident Response KYPO Environment

This repository contains a topology and Ansible playbooks for deploying an incident response lab. The setup is intended for use in the KYPO Cyber Range or similar environments.

## Contents

- `topology.yml` – defines the virtual machines, router and network layout.
- `provisioning/attacker-playbook.yml` – installs attacker tools like Metasploit, Nmap and copies an initial attack script.
- `provisioning/internal-server-playbook.yml` – provisions a vulnerable Apache server with sample data.
- `provisioning/soc-server-playbook.yml` – installs a SIEM stack along with TheHive, Cortex and MISP.
- `provisioning/user-pc-playbook.yml` – prepares a Windows workstation with PowerShell Remoting and Sysinternals.
- `provisioning/router-playbook.yml` – configures the router with IP forwarding and NAT.

## Usage

1. Create the virtual machines based on `topology.yml` in your cyber range.
2. Adjust `inventory.sample` with the correct credentials if needed.
3. Run the playbooks using this inventory file:

```bash
ansible-playbook -i inventory.sample provisioning/router-playbook.yml
ansible-playbook -i inventory.sample provisioning/attacker-playbook.yml
ansible-playbook -i inventory.sample provisioning/internal-server-playbook.yml
ansible-playbook -i inventory.sample provisioning/soc-server-playbook.yml
ansible-playbook -i inventory.sample provisioning/user-pc-playbook.yml
```

4. Verify the SOC services are running:

```bash
ansible-playbook -i inventory.sample provisioning/service-checks.yml
```

## Additional Materials

Screenshots and a lab document (`LM8-Operation IncidentResponse`) are provided for reference.

## Role Guides

The steps for each role are documented in the `docs/` directory:

- [SOC Analyst](docs/soc-analyst.md)
- [Incident Responder](docs/incident-responder.md)
- [CTI Analyst](docs/cti-analyst.md)
- [Pen Tester](docs/pen-tester.md)
- [IR Coordinator](docs/ir-coordinator.md)


## Importing into KYPO

1. Log in to your KYPO CRP instance and navigate to **Trainings**.
2. Click **Import training** and select `training_linear.json` from this repository.
3. The import references `topology.yml` and will create the required environment automatically.
4. Once imported, you can start the training from the KYPO web interface.

## Licence

This project is provided for educational purposes.
