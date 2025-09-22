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

## Criterios de evaluación
- Selección correcta del playbook CACAO en NG-SOC acorde a la clasificación inicial de la alerta.
- Ejecución completa de las acciones automatizadas en NG-SOAR sin fallos en los conectores críticos.
- Sincronización oportuna de los hitos en CICMS Operator, incluyendo evidencias y aprobaciones requeridas.
- Registro de las lecciones aprendidas en la biblioteca de playbooks, enlazando controles MITRE ATT&CK y referencias NVD/NIST aplicadas.

## Retroalimentación automática de la plataforma
- NG-SIEM genera un puntaje de calidad de detección basado en la precisión de la correlación y lo muestra en la consola de NG-SOC.
- NG-SOAR expone un informe de ejecución del playbook con métricas de éxito por tarea, destacando los pasos que requieren revisión.
- CICMS Operator alerta cuando un hito manual queda pendiente y conserva la trazabilidad necesaria para auditoría.
- La biblioteca de playbooks publica un resumen actualizado con referencias a MITRE ATT&CK, NVD/NIST y CTI reciente para incidentes futuros.
