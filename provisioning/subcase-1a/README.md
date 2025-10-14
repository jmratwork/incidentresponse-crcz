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

- Ansible 2.15 or newer with the `ansible.windows` and `community.general` collections installed, plus the `pywinrm` Python package for WinRM connectivity (use `pywinrm[credssp]` when the scenario requires CredSSP).
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

## Role functional requirements

### `rep_core`
- **Servicio**: publica la plataforma REP detrás de Nginx con equilibrio hacia los microservicios de `scheduler`, `live_session` y `quiz_engine`.
- **Configuración**: el archivo `templates/nginx-rep-core.conf.j2` genera el *virtual host* TLS y los *upstreams* definidos en `defaults/main.yml` (`rep_core_virtual_host` y `rep_core_tls`). También se protege un secreto compartido en `rep_core_shared_secret_file`.
- **Variables clave**: `rep_core_virtual_host.*`, `rep_core_tls.*`, `rep_core_shared_secret` y `rep_core_healthcheck` describen rutas, certificados y comprobaciones de salud.
- **Validación**: `tasks/main.yml` ejecuta `nginx -t` y una llamada `ansible.builtin.uri` al `healthcheck_path`, marcando error si el código HTTP difiere del esperado.

### `reporting_workspace`
- **Servicio**: aprovisiona Grafana con *datasources* PostgreSQL y paneles para supervisar el ejercicio.
- **Configuración**: las plantillas `grafana.ini.j2`, `datasources.yaml.j2`, `dashboards.yaml.j2` y `dashboard.json.j2` generan la configuración de Grafana y los paneles listados en `reporting_workspace_dashboards`.
- **Variables clave**: `reporting_workspace_datasources`, `reporting_workspace_dashboards`, `reporting_workspace_grafana_ini` y `reporting_workspace_healthcheck` permiten parametrizar puertos, paneles y pruebas.
- **Validación**: tras desplegar las plantillas se consulta `GET {{ reporting_workspace_healthcheck.url }}` esperando un `database == 'ok'`.

### `instructor_console`
- **Servicio**: prepara el terminal de la persona instructora con sesiones `tmux` predefinidas y atajos shell a los servicios críticos.
- **Configuración**: `tmux.conf.j2` y `instructor-console.sh.j2` traducen `instructor_console_tmux_settings` y `instructor_console_shortcuts` en archivos en `$HOME` y `/etc/profile.d`.
- **Variables clave**: `instructor_console_user`, `instructor_console_workspace`, `instructor_console_tmux_settings` y `instructor_console_shortcuts`.
- **Validación**: se ejecuta `tmux -f … display-message` y un `bash -lc` que verifica que los *shortcuts* queden definidos como funciones.

### `trainee_workstation`
- **Servicio**: distribuye la configuración del agente REP Collector, los accesos directos en los escritorios Windows de los participantes y el mensaje de bienvenida del laboratorio.
- **Configuración**: mediante `ansible.windows.win_template` se generan `collector.yaml` y los accesos `.url` descritos en `trainee_workstation_shortcuts`, y con `ansible.windows.win_copy` se publica la nota `WELCOME.txt` en `{{ trainee_workstation_welcome_note.directory }}`.
- **Variables clave**: `trainee_workstation_collector.*` (ruta, servicio y transportes), `trainee_workstation_shortcuts` y `trainee_workstation_welcome_note.*` (directorio, nombre y contenido del mensaje).
- **Validación**: se comprueba el servicio con `Get-Service` y se reinicia automáticamente si cambian las plantillas.

## Parametrización y comprobaciones

Cada rol expone su configuración predeterminada en `roles/<rol>/defaults/main.yml`. Ajuste esas variables en inventario, `group_vars` o parámetros `-e` para personalizar hosts, certificados, destinos de ingesta o accesos directos sin modificar las plantillas.

El archivo `tasks/main.yml` de cada rol aplica la configuración de forma idempotente mediante `ansible.builtin.template`/`ansible.windows.win_template` y registra *handlers* para reiniciar servicios cuando sea necesario. Las últimas tareas incorporan verificaciones post-configuración (comprobaciones HTTP, comandos `nginx -t`, `tmux`, `Get-Service`, etc.) con condiciones `failed_when` que detienen la ejecución si los servicios no responden como se espera.
