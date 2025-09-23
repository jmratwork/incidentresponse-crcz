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

- Ansible 2.15 or newer with the `community.general` collection available. Install the `pywinrm` Python package for WinRM connectivity when managing Windows hosts from the same control node (use `pywinrm[credssp]` where CredSSP is needed).
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

## Role functional requirements

### `cicms`
- **Servicio**: expone el portal de coordinación de incidentes con Nginx y enruta hacia el backend en `:9201`.
- **Configuración**: `nginx-cicms.conf.j2` y `settings.json.j2` convierten las variables `cicms_nginx_site`, `cicms_tls` y `cicms_cms_settings` en la configuración real y secretos TLS.
- **Validación**: `nginx -t` y una solicitud `GET {{ cicms_healthcheck.url }}` aseguran que el *virtual host* responda.

### `cti_ss`
- **Servicio**: publica un servidor TAXII con colecciones STIX utilizadas por NG-SIEM y NG-SOAR.
- **Configuración**: `taxii.yaml.j2` toma `cti_ss_taxii_collections`, credenciales y puertos para generar `/etc/cti-ss/taxii.yaml`.
- **Validación**: `cti-ssctl configtest` y `cti_ss_healthcheck_command` comprueban sintaxis y estado del daemon.

### `ng_siem`
- **Servicio**: mantiene el *pipeline* `rep_ingest` con fuentes TCP y TAXII, enriquecimientos GeoIP y salida a Elasticsearch.
- **Configuración**: `pipeline.conf.j2` traduce `ng_siem_pipeline` en el archivo de `pipelines.d`.
- **Validación**: se ejecuta `ng-siemctl pipeline lint` seguido de `ng_siem_healthcheck.command` para verificar que la canalización esté saludable.

### `ng_soar`
- **Servicio**: define colas de orquestación y conectores (REST/Kafka) para la automatización NG-SOAR.
- **Configuración**: `queues.yaml.j2` usa `ng_soar_queues` y `ng_soar_integrations` para publicar la topología de colas.
- **Validación**: `ng-soarctl validate` y una comprobación HTTP `{{ ng_soar_healthcheck.url }}`.

### `ng_soc`
- **Servicio**: entrega el tablero del SOC con widgets conectados a NG-SIEM/NG-SOAR y rutas de alerta.
- **Configuración**: `dashboard.yaml.j2` consume `ng_soc_widgets` y `ng_soc_alert_routes` para construir `/etc/ng-soc/dashboard.yaml`.
- **Validación**: `ng-socctl validate` y `ansible.builtin.uri` contra `ng_soc_healthcheck.url`.

### `playbook_library`
- **Servicio**: aloja los playbooks CACAO consumidos por NG-SOAR.
- **Configuración**: las plantillas `playbook.json.j2` e `index.json.j2` serializan `playbook_library_playbooks` en archivos individuales y un índice general.
- **Validación**: `playbook_library_healthcheck_command` (por defecto `cacaoctl validate`).

### `telemetry_feeder`
- **Servicio**: distribuye el agente que envía telemetría y observables a NG-SIEM y CTI-SS.
- **Configuración**: `agent.yaml.j2` refleja `telemetry_feeder_agent` con *buffers*, transformaciones y salidas.
- **Validación**: `telemetry-feederctl lint` más una consulta HTTP contra `telemetry_feeder_healthcheck_url`.

## Parametrización y comprobaciones

Las variables predeterminadas viven en `roles/<rol>/defaults/main.yml` y cubren puertos, rutas de plantillas, parámetros CACAO y credenciales de ingesta. Ajuste esos valores en `group_vars`, inventario o `--extra-vars` para adaptar pipelines, colas y colecciones a cada laboratorio.

Cada `tasks/main.yml` aplica las plantillas con módulos idempotentes (`ansible.builtin.template`, `ansible.builtin.copy`) y activa *handlers* para reinicios controlados. Los pasos finales incluyen validaciones de línea de comandos o `ansible.builtin.uri` con `failed_when` explícitos, de modo que cualquier fallo en la conectividad, sintaxis o estado del servicio detiene el despliegue y proporciona trazabilidad inmediata.
