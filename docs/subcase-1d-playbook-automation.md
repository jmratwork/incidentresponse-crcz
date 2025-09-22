# Subcaso 1d – Automatización de Playbooks en el ecosistema NG-SOC

Este documento resume las actividades que se desarrollan en el entorno operativo integrado por NG-SOC, NG-SIEM, NG-SOAR, el operador CICMS, CTI-SS y la biblioteca de playbooks/estándares (NVD/NIST, MITRE ATT&CK) durante la ejecución del subcaso 1d.

## Flujo operativo
1. **Generación de alerta en NG-SIEM**
   - NG-SIEM correlaciona eventos de telemetría y produce una alerta priorizada que incluye indicadores clave y activos afectados.
   - La alerta se envía a la consola de NG-SOC junto con las recomendaciones iniciales basadas en reglas de correlación.
2. **Validación en NG-SOC**
   - El analista revisa la alerta, selecciona el playbook CACAO adecuado desde el repositorio de NG-SOC y define los parámetros de ejecución.
   - Se contrasta la selección con la biblioteca de playbooks/estándares para asegurar cobertura frente a MITRE ATT&CK y referencias NVD/NIST.
3. **Orquestación mediante NG-SOAR**
   - NG-SOC orquesta la ejecución delegando en NG-SOAR, que interpreta la secuencia CACAO y coordina tareas automáticas.
   - Los conectores de NG-SOAR consultan CTI-SS para enriquecer indicadores y validar reputación.
4. **Coordinación con CICMS Operator**
   - Cuando el playbook requiere intervenciones manuales o validaciones, NG-SOAR sincroniza los hitos con el operador CICMS.
   - CICMS Operator consolida evidencias, actualiza el estado del incidente y prepara el reporte post-incidente.
5. **Documentación y aprendizaje con la biblioteca de playbooks**
   - Al finalizar cada fase, NG-SOAR publica los resultados en NG-SOC y NG-SIEM, mientras que CICMS Operator anota las decisiones relevantes.
   - Se actualizan las referencias de la biblioteca (MITRE ATT&CK, NVD/NIST) con lecciones aprendidas y enlaces a CTI reciente.

## Ejercicios prácticos
### Ejercicio 1: Ransomware en infraestructura crítica
- **Objetivo:** validar la detección temprana y la contención automática de un ataque de cifrado masivo.
- **Fases operativas:**
  1. *Detección*: NG-SIEM identifica patrones de cifrado anómalos y genera la alerta priorizada.
  2. *Contención*: NG-SOAR ejecuta el playbook CACAO para aislar los endpoints críticos y revocar credenciales sospechosas.
  3. *Recuperación*: CICMS coordina con los equipos de continuidad para restaurar respaldos y verificar integridad.
- **Interacción de plataformas:** NG-SIEM alimenta a NG-SOAR con artefactos para automatizar la respuesta; NG-SOAR invoca conectores resilientes hacia CTI-SS para validar indicadores y hacia la biblioteca de playbooks para confirmar la cobertura MITRE ATT&CK; CICMS documenta las decisiones y actualiza el estado de recuperación, mientras NG-SOC supervisa la ejecución de extremo a extremo.

### Ejercicio 2: Exfiltración de datos mediante canal cifrado
- **Objetivo:** asegurar que el ecosistema coordine la investigación y bloqueo de comunicaciones maliciosas hacia servicios externos.
- **Fases operativas:**
  1. *Correlación*: NG-SIEM cruza flujos de red con inteligencia CTI-SS para identificar direcciones de comando y control.
  2. *Orquestación*: NG-SOC selecciona el playbook CACAO que instruye a NG-SOAR para desplegar reglas de firewall y solicitar evidencia a herramientas de DLP.
  3. *Análisis y cierre*: CICMS centraliza la evidencia, mientras la biblioteca de playbooks almacena los indicadores para futuras referencias.
- **Interacción de plataformas:** NG-SOAR mantiene conectores redundantes hacia dispositivos de red para garantizar la aplicación de bloqueos; CTI-SS aporta indicadores enriquecidos; CICMS registra las aprobaciones y el racional técnico, y NG-SOC ajusta la estrategia basándose en los informes provenientes de NG-SIEM y NG-SOAR.

### Ejercicio 3: Compromiso de credenciales privilegiadas
- **Objetivo:** evaluar la capacidad de detección, respuesta y remediación de accesos privilegiados comprometidos.
- **Fases operativas:**
  1. *Alerta inicial*: NG-SIEM detecta actividad sospechosa en cuentas privilegiadas con base en anomalías de comportamiento.
  2. *Respuesta coordinada*: NG-SOC selecciona un playbook de rotación de credenciales que NG-SOAR ejecuta para revocar accesos, generar credenciales temporales y notificar a los responsables.
  3. *Verificación y lecciones*: CICMS valida que se restablecieron los controles, mientras la biblioteca de playbooks incorpora las mejoras y CTI-SS añade firmas relacionadas.
- **Interacción de plataformas:** NG-SOAR asegura la resiliencia de los conectores hacia los sistemas de gestión de identidades; NG-SIEM monitorea los eventos posteriores a la rotación; CICMS actualiza la documentación y las métricas de impacto, y NG-SOC utiliza la biblioteca de playbooks para proponer ajustes estratégicos y generar entrenamiento adicional.

## Criterios de evaluación
- Selección correcta del playbook CACAO en NG-SOC acorde a la clasificación inicial de la alerta.
- Ejecución completa de las acciones automatizadas en NG-SOAR sin fallos en los conectores críticos.
- Sincronización oportuna de los hitos en CICMS Operator, incluyendo evidencias y aprobaciones requeridas.
- Registro de las lecciones aprendidas en la biblioteca de playbooks, enlazando controles MITRE ATT&CK y referencias NVD/NIST aplicadas.
- Resiliencia de los conectores orquestados por NG-SOAR y NG-SOC, validando redundancias y planes de contingencia documentados.
- Documentación exhaustiva en CICMS Operator, incluyendo procedimientos seguidos, indicadores finales y responsables de cada acción.
- Incorporación y seguimiento de métricas post-incidente (tiempo de contención, tiempo de recuperación, impacto residual) registradas en NG-SIEM, NG-SOAR y CICMS.

## Retroalimentación automática de la plataforma
- NG-SIEM genera un puntaje de calidad de detección basado en la precisión de la correlación y lo muestra en la consola de NG-SOC.
- NG-SOAR expone un informe de ejecución del playbook con métricas de éxito por tarea, destacando los pasos que requieren revisión.
- CICMS Operator alerta cuando un hito manual queda pendiente y conserva la trazabilidad necesaria para auditoría.
- La biblioteca de playbooks publica un resumen actualizado con referencias a MITRE ATT&CK, NVD/NIST y CTI reciente para incidentes futuros.
- Los conectores monitoreados por NG-SOAR reportan indicadores de resiliencia (latencia, disponibilidad, reintentos) para facilitar ajustes preventivos.
- CICMS Operator genera recordatorios automáticos para completar la documentación pendiente y contrastarla con los lineamientos internos.
- Se calculan métricas post-incidente consolidadas (MTTD, MTTR, eficacia de contención) y se comparan con umbrales definidos dentro de la biblioteca de playbooks.
