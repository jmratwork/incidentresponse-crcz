# Procedimientos automatizados para playbooks CACAO en NG-SOAR

Este documento reemplaza los scripts de despliegue tradicionales y describe cómo automatizar el ciclo de vida de los playbooks CACAO dentro de NG-SOAR, garantizando su sincronización con CICMS Operator, CTI-SS y la biblioteca de playbooks. Las automatizaciones se basan en API disponibles en los componentes del Subcaso 1d y pueden ejecutarse desde cualquier consola con acceso autenticado.

## 1. Creación de playbooks

```bash
#!/usr/bin/env bash
# crear_playbook.sh
# Uso: ./crear_playbook.sh ruta/al/playbook.json
set -euo pipefail
PLAYBOOK_PATH="$1"
TOKEN=$(http POST https://ng-soc.example/api/auth username=$SOC_USER password=$SOC_PASS | jq -r '.token')

http POST https://ng-soc.example/api/cacao/repository \
  "Authorization: Bearer $TOKEN" \
  < "$PLAYBOOK_PATH"

http POST https://ng-soar.example/api/playbooks/import \
  "Authorization: Bearer $TOKEN" \
  < "$PLAYBOOK_PATH"

http POST https://cicms.example/api/incidents/register-playbook \
  "Authorization: Bearer $TOKEN" \
  playbook_path="$PLAYBOOK_PATH"
```

- La primera llamada registra el playbook en el repositorio central de NG-SOC.
- La segunda llamada lo importa en NG-SOAR para quedar disponible en las colas de ejecución.
- La tercera registra el material en CICMS Operator para que el equipo operativo disponga del contexto actualizado.
- Cada script de creación debe almacenarse junto con las referencias correspondientes en la biblioteca de playbooks.

## 2. Actualización y versionado

```bash
#!/usr/bin/env bash
# actualizar_playbook.sh
# Uso: ./actualizar_playbook.sh identificador ruta/al/playbook.json
set -euo pipefail
PLAYBOOK_ID="$1"
PLAYBOOK_PATH="$2"
TOKEN=$(http POST https://ng-soc.example/api/auth username=$SOC_USER password=$SOC_PASS | jq -r '.token')

http PUT https://ng-soc.example/api/cacao/repository/$PLAYBOOK_ID \
  "Authorization: Bearer $TOKEN" \
  < "$PLAYBOOK_PATH"

http PUT https://ng-soar.example/api/playbooks/$PLAYBOOK_ID \
  "Authorization: Bearer $TOKEN" \
  < "$PLAYBOOK_PATH"

http POST https://playbooks.example/api/library/register \
  "Authorization: Bearer $TOKEN" \
  playbook_id="$PLAYBOOK_ID" \
  version="$(jq -r '.version' "$PLAYBOOK_PATH")" \
  references="MITRE ATT&CK,NVD,NIST"
```

- La actualización sincroniza NG-SOC y NG-SOAR con la nueva versión y registra el cambio en la biblioteca de playbooks.
- La biblioteca conserva el historial de versiones y las notas de publicación.

## 3. Distribución y compartición con CTI-SS

```bash
#!/usr/bin/env bash
# compartir_playbook.sh
# Uso: ./compartir_playbook.sh identificador canal_ctiss
set -euo pipefail
PLAYBOOK_ID="$1"
CHANNEL="$2"
TOKEN=$(http POST https://ng-soc.example/api/auth username=$SOC_USER password=$SOC_PASS | jq -r '.token')

PAYLOAD=$(http GET https://ng-soar.example/api/playbooks/$PLAYBOOK_ID \
  "Authorization: Bearer $TOKEN")

http POST https://cti-ss.example/api/cacao/share \
  "Authorization: Bearer $TOKEN" \
  channel="$CHANNEL" \
  payload="$PAYLOAD"
```

- NG-SOAR expone el playbook en formato CACAO y CTI-SS lo replica hacia los canales de inteligencia específicos.
- CTI-SS añade etiquetas y taxonomías antes de redistribuir el contenido.
- El proceso queda registrado en CICMS Operator y en la biblioteca para mantener la trazabilidad.

## 4. Integraciones con CICMS Operator y la biblioteca de playbooks
- Cada script registra metadatos en CICMS Operator y en la biblioteca (`/library/register`) para mantener la trazabilidad.
- Los responsables de NG-SOC revisan semanalmente el tablero de CICMS Operator para validar que no existan discrepancias entre versiones.
- Cuando un playbook alcanza estado estable, se crea un resumen en la biblioteca con referencia a las fuentes de CTI-SS empleadas.

## 5. Sustitución de la infraestructura KYPO
- Estas automatizaciones se ejecutan dentro del propio ecosistema NG y eliminan la dependencia de la infraestructura KYPO.
- No se requieren máquinas externas ni despliegues adicionales: basta con credenciales de servicio y conectividad segura.
- La documentación y scripts se alojan en la biblioteca de playbooks asociada al Subcaso 1d.
