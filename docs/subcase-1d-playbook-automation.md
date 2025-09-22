# Subcaso 1d – Automatización de Playbooks en el ecosistema NG-SOC

Este documento resume las actividades que se desarrollan en el entorno operativo integrado por NG-SOC, NG-SIEM, NG-SOAR, BPMS, CMDB, CTI-SS y KMS durante la ejecución del subcaso 1d.

## Flujo operativo
1. **Generación de alerta en NG-SIEM**
   - NG-SIEM correlaciona eventos de telemetría y produce una alerta priorizada que incluye indicadores clave y activos afectados.
   - La alerta se envía a la consola de NG-SOC junto con las recomendaciones iniciales basadas en reglas de correlación.
2. **Validación en NG-SOC**
   - El analista revisa la alerta, selecciona el playbook CACAO adecuado desde el repositorio de NG-SOC y define los parámetros de ejecución.
   - Se asigna la severidad y se registran las dependencias relevantes consultando la CMDB.
3. **Orquestación mediante NG-SOAR**
   - NG-SOC orquesta la ejecución delegando en NG-SOAR, que interpreta la secuencia CACAO y coordina tareas automáticas y manuales.
   - Los conectores de NG-SOAR consultan CTI-SS para enriquecer indicadores y validar reputación.
4. **Gestión de actividades humanas con BPMS**
   - Cuando el playbook requiere intervenciones manuales, NG-SOAR crea tareas en BPMS para los grupos responsables.
   - BPMS controla aprobaciones, recoge evidencias y notifica a NG-SOAR cuando se completan los hitos.
5. **Documentación y aprendizaje en KMS**
   - Al finalizar cada fase, NG-SOAR publica los resultados en NG-SOC y NG-SIEM, mientras que BPMS actualiza el estado administrativo.
   - KMS recibe automáticamente los procedimientos ejecutados, indicadores finales y lecciones aprendidas validadas por el analista.

## Criterios de evaluación
- Selección correcta del playbook CACAO en NG-SOC acorde a la clasificación inicial de la alerta.
- Ejecución completa de las acciones automatizadas en NG-SOAR sin fallos en los conectores críticos.
- Cumplimiento de las tareas asignadas en BPMS dentro de los tiempos definidos por el flujo.
- Actualización de la CMDB con la información del activo principal y registro en KMS de las lecciones aprendidas.

## Retroalimentación automática de la plataforma
- NG-SIEM genera un puntaje de calidad de detección basado en la precisión de la correlación y lo muestra en la consola de NG-SOC.
- NG-SOAR expone un informe de ejecución del playbook con métricas de éxito por tarea, destacando los pasos que requieren revisión.
- BPMS envía notificaciones automáticas cuando una tarea supera el tiempo objetivo y registra la trazabilidad completa para auditoría.
- KMS publica un resumen de conocimiento con indicadores de reutilización sugeridos para incidentes futuros, señalando brechas de documentación.
