# Automated procedures for CACAO playbooks in NG-SOAR

This document replaces traditional deployment scripts and explains how to automate the lifecycle of CACAO playbooks within NG-SOAR, ensuring synchronisation with CICMS Operator, CTI-SS and the playbook library. The automations rely on APIs available in the Subcase 1d components and can be run from any console with authenticated access.

> **Prerequisites:** the examples use [HTTPie](https://httpie.io/) with the `--check-status` and `--print=b` (`-b`) options to ensure that any post-processing, such as `jq`, operates solely on the JSON body returned by the API and so that scripts fail on unsuccessful HTTP codes.

## 1. Playbook creation

```bash
#!/usr/bin/env bash
# crear_playbook.sh
# Usage: ./crear_playbook.sh path/to/playbook.json
set -euo pipefail
PLAYBOOK_PATH="$1"
TOKEN=$(http --check-status --print=b POST https://ng-soc.example/api/auth username=$SOC_USER password=$SOC_PASS | jq -r '.token')

http --check-status POST https://ng-soc.example/api/cacao/repository \
  "Authorization: Bearer $TOKEN" \
  < "$PLAYBOOK_PATH"

http --check-status POST https://ng-soar.example/api/playbooks/import \
  "Authorization: Bearer $TOKEN" \
  < "$PLAYBOOK_PATH"

http --check-status POST https://cicms.example/api/incidents/register-playbook \
  "Authorization: Bearer $TOKEN" \
  playbook_path="$PLAYBOOK_PATH"
```

- The first call registers the playbook in the NG-SOC central repository.
- The second call imports it into NG-SOAR so it is available in the execution queues.
- The third records the material in CICMS Operator so the operations team has the latest context.
- Each creation script should be stored together with the corresponding references in the playbook library.

## 2. Updating and versioning

```bash
#!/usr/bin/env bash
# actualizar_playbook.sh
# Usage: ./actualizar_playbook.sh identifier path/to/playbook.json
set -euo pipefail
PLAYBOOK_ID="$1"
PLAYBOOK_PATH="$2"
TOKEN=$(http --check-status --print=b POST https://ng-soc.example/api/auth username=$SOC_USER password=$SOC_PASS | jq -r '.token')

http --check-status PUT https://ng-soc.example/api/cacao/repository/$PLAYBOOK_ID \
  "Authorization: Bearer $TOKEN" \
  < "$PLAYBOOK_PATH"

http --check-status PUT https://ng-soar.example/api/playbooks/$PLAYBOOK_ID \
  "Authorization: Bearer $TOKEN" \
  < "$PLAYBOOK_PATH"

http --check-status POST https://playbooks.example/api/library/register \
  "Authorization: Bearer $TOKEN" \
  playbook_id="$PLAYBOOK_ID" \
  version="$(jq -r '.version' "$PLAYBOOK_PATH")" \
  references="MITRE ATT&CK,NVD,NIST"
```

- The update synchronises NG-SOC and NG-SOAR with the new version and records the change in the playbook library.
- The library keeps the version history and the release notes.

## 3. Distribution and sharing with CTI-SS

```bash
#!/usr/bin/env bash
# compartir_playbook.sh
# Usage: ./compartir_playbook.sh identifier ctiss_channel
set -euo pipefail
PLAYBOOK_ID="$1"
CHANNEL="$2"
TOKEN=$(http --check-status --print=b POST https://ng-soc.example/api/auth username=$SOC_USER password=$SOC_PASS | jq -r '.token')

PAYLOAD=$(http --check-status --print=b GET https://ng-soar.example/api/playbooks/$PLAYBOOK_ID \
  "Authorization: Bearer $TOKEN")

http --check-status POST https://cti-ss.example/api/cacao/share \
  "Authorization: Bearer $TOKEN" \
  channel="$CHANNEL" \
  payload:="$PAYLOAD"
```

- NG-SOAR exposes the playbook in CACAO format and CTI-SS replicates it to the targeted intelligence channels.
- Nota: el uso de `:=` en HTTPie evita re-escapar el JSON y lo reenvía íntegro a CTI-SS.
- CTI-SS adds tags and taxonomies before redistributing the content.
- The process is logged in CICMS Operator and in the library to maintain traceability.

## 4. Integrations with CICMS Operator and the playbook library
- Each script records metadata in CICMS Operator and in the library (`/library/register`) to preserve traceability.
- NG-SOC leads review of the CICMS Operator dashboard every week to confirm there are no discrepancies between versions.
- When a playbook reaches a stable state, a summary is created in the library with references to the CTI-SS sources used.

## 5. Replacement of the KYPO infrastructure
- These automations run within the NG ecosystem itself and remove the dependency on the KYPO infrastructure.
- No external machines or additional deployments are required: service credentials and secure connectivity are sufficient.
- Documentation and scripts are hosted in the playbook library associated with Subcase 1d.
