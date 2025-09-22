# Subcase 1d – Provisioning guide

Automation assets for the NG-SOC ecosystem used during the playbook execution exercises. Each role prepares the baseline required to validate the end-to-end flow between NG-SIEM, NG-SOC, NG-SOAR, CTI-SS, CICMS Operator and the playbook library.

## Host groups

| Inventory group | Hosts | Purpose |
| --- | --- | --- |
| `ng_soc` | `ng-soc` | Analyst console and orchestration entry point. |
| `ng_siem` | `ng-siem` | Event correlation and alerting platform. |
| `ng_soar` | `ng-soar` | Automation engine running CACAO playbooks. |
| `cti_ss` | `cti-ss` | Threat intelligence and indicator enrichment. |
| `cicms` | `cicms-operator` | Incident coordination and documentation workspace. |
| `playbook_library` | `playbook-library` | Standards repository (NVD/NIST, MITRE ATT&CK) and lessons learnt. |
| `telemetry_feeder` | `telemetry-simulator` | Generates telemetry samples for NG-SIEM validation. |

## Requirements

- Ansible 2.15 or newer with the `community.general` collection available.
- Access to the hosts defined in `provisioning/subcase-1d-topology.yml`.
- Secrets managed through Ansible Vault or environment variables.

Install the collection with:

```bash
ansible-galaxy collection install community.general
```

## Running the playbook

```bash
ansible-playbook -i inventory.ini provisioning/subcase-1d/site.yml
```

Use tags to execute individual components, e.g. `--tags ng_siem` to provision only the SIEM server.

## Variables

- `ng_soc_packages` (default `['docker.io', 'python3-pip']`)
- `ng_siem_packages` (default `['openjdk-17-jdk', 'rsyslog']`)
- `ng_soar_packages` (default `['python3-venv', 'redis-server']`)
- `cti_ss_packages` (default `['python3-requests', 'jq']`)
- `cicms_packages` (default `['postgresql-client', 'curl']`)
- `playbook_library_packages` (default `['git', 'nginx']`)
- `telemetry_feeder_packages` (default `['python3-venv', 'rsyslog']`)

Set them per group to adapt the stack to each exercise iteration.
