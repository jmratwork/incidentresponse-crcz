# Habilitación de la Random Education Platform y servicios NG del Subcaso 1d

Este artefacto describe las actividades necesarias para disponer de la Random Education Platform (REP) y de los servicios NG-SOC, NG-SIEM, NG-SOAR, CICMS Operator, CTI-SS y la biblioteca de playbooks durante las prácticas del Subcaso 1d. La información se presenta como procedimientos de activación y no como instrucciones de despliegue desde cero; se asume que los componentes existen en el CyberRangeCZ y requieren únicamente configuración y conexión.

## Random Education Platform (REP)
1. **Verificar módulos activos**: habilitar *Scheduler*, *Live Session*, *Quiz Engine* y *Practical Labs* desde el panel de administración.
2. **Conectar con el instructor**: vincular la consola del instructor y la zona de reporting seleccionando la clase correspondiente en el calendario.
3. **Sincronizar simuladores**: confirmar que los simuladores de CyberRangeCZ estén publicados como laboratorios dentro de la REP y asignarlos al itinerario del ejercicio.

## NG-SOC
1. **Activar la recepción de alertas** desde NG-SIEM habilitando el canal seguro `soc-siem`.
2. **Sincronizar playbooks CACAO** con NG-SOAR mediante la API `soar-repository/sync` para garantizar que las versiones validadas estén disponibles.
3. **Exponer panel operativo** enlazando la biblioteca de playbooks como fuente de conocimiento para consultas en tiempo real.

## NG-SIEM
1. **Seleccionar fuentes de telemetría** asociadas al laboratorio y asegurarse de que la clasificación de eventos coincide con los escenarios del Subcaso 1d.
2. **Publicar reglas de correlación** específicas que generen alertas priorizadas hacia NG-SOC.
3. **Habilitar intercambio con CTI-SS** para enriquecer automáticamente los incidentes con inteligencia de amenazas vigente.

## NG-SOAR
1. **Importar playbooks CACAO** recibidos desde NG-SOC y validar su integridad en el repositorio interno.
2. **Configurar conectores** hacia CICMS Operator, CTI-SS y la biblioteca de playbooks asegurando credenciales de servicio y certificados actualizados.
3. **Definir colas de ejecución** para separar tareas automáticas de las que requieren intervención manual supervisada por CICMS Operator.

## CICMS Operator
1. **Registrar procesos de apoyo** vinculados a los playbooks CACAO (aprobaciones, revisiones, tareas de campo) dentro del flujo operativo.
2. **Establecer SLA y notificaciones** para cada actividad manual, direccionando las alertas a los grupos operativos de NG-SOC.
3. **Sincronizar el panel de seguimiento** con NG-SOAR para recibir hitos de ejecución y devolver confirmaciones de cierre.

## CTI-SS
1. **Seleccionar fuentes de inteligencia** relevantes al ejercicio y actualizar los feeds de indicadores.
2. **Publicar taxonomías y etiquetas** que NG-SOAR utilizará para clasificar indicadores durante el enriquecimiento.
3. **Sincronizar conocimiento con la biblioteca de playbooks** para que las lecciones aprendidas incorporen contexto de amenazas vigente.

## Biblioteca de playbooks/estándares
1. **Definir el espacio de conocimiento** del Subcaso 1d, incorporando referencias MITRE ATT&CK, NVD y NIST aplicables.
2. **Configurar integraciones** para recibir datos de NG-SOC, NG-SOAR y CICMS Operator mediante conectores autenticados.
3. **Habilitar versionado** automático de documentos para conservar la evolución de los playbooks y procedimientos.

## Validación final
- Revisar desde NG-SOC que todos los componentes respondan a pruebas de conectividad.
- Ejecutar un playbook CACAO de verificación y confirmar que CICMS Operator, CTI-SS y la biblioteca de playbooks registran actividad.
- Documentar los resultados en CICMS Operator y notificar a los responsables del ejercicio.
