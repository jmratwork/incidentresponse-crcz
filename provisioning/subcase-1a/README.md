# Subcase 1a – Provisioning guide

The playbooks in this directory prepare the infrastructure required by the phishing awareness exercises delivered on the Random Education Platform (REP).

## Host groups

| Inventory group | Hosts | Purpose |
| --- | --- | --- |
| `rep_core` | `rep-scheduler`, `rep-live-session`, `rep-quiz-engine`, `rep-practical-labs` | Backend services that coordinate course scheduling, live delivery, quizzes and practical labs. |
| `reporting_workspace` | `reporting-workspace` | Dashboards and report consolidation workspace. |
| `instructor_console` | `instructor-console` | Entry point for instructors to manage the live session. |
| `trainees` | `trainee-workstation-01`, `trainee-workstation-02` | Windows workstations used by participants during the labs. |

## Requirements

- Ansible 2.15 or newer with the `ansible.windows` and `community.general` collections installed.
- Network reachability towards the hosts defined in `provisioning/subcase-1a-topology.yml`.
- Credentials provided through Ansible Vault files or environment variables (see `inventory.sample`).

Install the collections with:

```bash
ansible-galaxy collection install ansible.windows community.general
```

## Running the playbook

1. Export sensitive variables or prepare an Ansible Vault file that contains the required passwords.
2. Copy `inventory.sample` to `inventory.ini` (or keep the `.sample` file) and adjust the host addresses if necessary.
3. Execute the site playbook:

```bash
ansible-playbook -i inventory.ini provisioning/subcase-1a/site.yml
```

## Variables

The roles expect the following optional variables that can be set in inventory or extra vars:

- `rep_core_packages`: list of additional packages for the REP backend servers (defaults to `['nginx', 'python3-venv']`).
- `reporting_workspace_packages`: analytics tooling to install (defaults to `['postgresql', 'grafana']`).
- `instructor_console_packages`: productivity tooling for the instructor (defaults to `['tmux', 'htop']`).
- `trainee_workspace_resources`: folders created on Windows workstations (defaults to `['C:\\Labs', 'C:\\Labs\\Evidence']`).

Override them by passing `-e` or defining group variables as required by the exercise scenario.
