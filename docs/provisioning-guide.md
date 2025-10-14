# Provisioning workflow for subcases 1a and 1d

This guide explains how to automate the lifecycle of the CyberRangeCZ topologies that back subcases 1a and 1d. The workflow now
includes a Python CLI that talks to KYPO, helper automation to combine API calls and Ansible, and the original manual steps for
reference.

## 1. Configure the KYPO CLI

1. Copy `tools/kypo_cli/config.sample.yaml` to `config.yaml` (or any file of your choice).
2. Edit the file to match your KYPO environment: portal URL, realm, username and password, client ID/secret, TLS verification
   preference and sandbox defaults.
3. You can override or replace these values with environment variables. The CLI looks for the following keys, using the `KYPO_`
   prefix by default:
   - `KYPO_PORTAL_URL`, `KYPO_REALM`, `KYPO_USERNAME`, `KYPO_PASSWORD`, `KYPO_CLIENT_ID`, `KYPO_CLIENT_SECRET`.
   - `KYPO_VERIFY_TLS` (set to `false` to skip certificate validation in test ranges).
   - `KYPO_TOKEN_ENDPOINT`, `KYPO_TOPOLOGY_ENDPOINT`, `KYPO_SANDBOX_ENDPOINT` to customise the API paths.
   - `KYPO_CONFIG` to point at an alternate configuration file.

### Example configuration

```yaml
portal_url: https://kypo.example.com
realm: academy
username: your.username
password: your-password
client_id: kypo-web
verify_tls: true
sandbox_defaults:
  name: incident-response-sandbox
  auto_start: true
```

## 2. Import topologies and deploy sandboxes with the CLI

### Using the low-level CLI

1. Authenticate and upload a topology:

   ```bash
   python -m tools.kypo_cli.cli --config config.yaml upload-topology provisioning/subcase-1a-topology.yml
   ```

   Replace the path with `provisioning/subcase-1d-topology.yml` for subcase 1d. The command prints the JSON returned by KYPO; the
   topology identifier is required for the next step.

2. Deploy a sandbox from the imported topology:

   ```bash
   python -m tools.kypo_cli.cli --config config.yaml deploy-sandbox <topology_id> --overrides '{"name": "subcase-1a"}'
   ```

   Use `--overrides` to extend the payload with extra KYPO parameters (for example, scheduling, capacity or access policies).

### Using the combined provisioning script

Run `tools/provision_subcase.py` to upload the relevant topology, trigger the sandbox and execute the matching Ansible playbook in
one go:

```bash
python tools/provision_subcase.py --subcase 1a --config config.yaml
```

Flags of interest:

- `--subcase`: choose `1a` or `1d`.
- `--sandbox-name`: override the sandbox name without crafting JSON.
- `--sandbox-overrides`: inject a JSON object into the deployment payload.
- `--inventory`: select an inventory file (defaults to `inventory.sample`).
- `--ansible-extra-args`: pass additional flags to `ansible-playbook` (for example `--ansible-extra-args "--tags setup"`).
- `--skip-kypo` or `--skip-ansible`: run only one part of the workflow.

## 3. Understand what each topology provisions

- `provisioning/subcase-1a-topology.yml` defines the REP backend servers, instructor and trainee workstations and the reporting
  workspace segments.
- `provisioning/subcase-1d-topology.yml` spins up the NG-SOC core (`ng-soc`, `ng-siem`, `ng-soar`) and supporting services for the
  automation and intelligence layers.

## 4. Prepare credentials for Ansible

1. Copy `inventory.sample` to `inventory.ini` (or keep the sample file and pass it explicitly).
2. Replace placeholder values with the IP addresses defined in the KYPO deployment, if needed.
3. Export credentials as environment variables before running the playbooks:

   ```bash
   export ANSIBLE_PASSWORD_REP_SCHEDULER='********'
   export ANSIBLE_PASSWORD_NG_SOC='********'
   ```

   You can also migrate the secrets to Ansible Vault variables if your security policy requires encrypted files.

## 5. Run the playbooks manually (optional)

The provisioning script already runs Ansible, but you can trigger the playbooks directly:

```bash
ansible-playbook -i inventory.ini provisioning/subcase-1a/site.yml
ansible-playbook -i inventory.ini provisioning/subcase-1d/site.yml
```

Install dependencies with:

```bash
python3 -m pip install --upgrade ansible
python3 -m pip install "pywinrm[credssp]"
ansible-galaxy collection install ansible.windows community.general
```

## 6. Validation steps

- Run `ansible all -i inventory.ini -m ping` (or `ansible -i inventory.ini windows -m ansible.windows.win_ping`) to validate
  connectivity.
- Confirm that key services are running, such as `nginx` on the playbook library, `redis-server` on NG-SOAR and Grafana on the
  reporting workspace.
- Execute `/opt/telemetry-simulator/scenarios/generate.sh` to verify that NG-SIEM receives events via `rsyslog`.
- Confirm that trainees can access `WELCOME.txt` in `C:\\Labs` and that the instructor console shows the `rep-notes` workspace.

## 7. Integrate with CI/CD pipelines

1. Store the KYPO credentials in the pipeline secret manager and inject them as `KYPO_*` environment variables or as a protected
   `config.yaml` artifact.
2. Add a job that checks out the repository, installs `requests` (for the CLI) and Ansible, and runs
   `python tools/provision_subcase.py --subcase <id> --skip-ansible` to pre-provision the sandbox.
3. Follow up with another job that executes Ansible against the freshly deployed sandbox using `--skip-kypo` to avoid duplicate
   deployments.
4. Capture the CLI JSON output as build artifacts so that sandbox identifiers are available for downstream testing or teardown
   stages.

Automating the provisioning pipeline in this way ensures that environments for subcases 1a and 1d can be reproduced reliably in
KYPO while keeping configuration details in version control.
