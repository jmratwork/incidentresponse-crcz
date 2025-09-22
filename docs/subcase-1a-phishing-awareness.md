# Subcaso 1a – Phishing Awareness en la Random Education Platform

Esta guía describe las actividades que el instructor y los/las trainees realizan dentro de la Random Education Platform (REP) para el módulo de concienciación frente a phishing. El flujo mantiene la correspondencia con los componentes documentados en la arquitectura de CyberRangeCZ.

## Preparación del curso por el instructor
- **Planificación en la consola del instructor**: se definen los objetivos del módulo y se asignan los recursos necesarios desde el repositorio de contenidos de CyberRangeCZ.
- **Programación en REP Scheduler**: el instructor crea el curso temático y activa los bloques de teoría, ejercicios guiados y prácticas sobre análisis de correos sospechosos.
- **Sincronización con el Reporting Workspace**: se configuran los tableros de métricas que recibirán los resultados de cuestionarios y laboratorios.

## Desarrollo de la sesión
1. **Apertura en REP Live Session**
   - El instructor inicia la sesión en vivo, comparte las reglas del ejercicio y habilita los canales colaborativos integrados (chat, videoconferencia y pizarra).
   - Las estaciones de trabajo de los/las trainees reciben el itinerario personalizado con cápsulas teóricas y recordatorios de buenas prácticas.
2. **Cuestionarios en REP Quiz Engine**
   - Cada trainee responde cuestionarios formativos que evalúan conceptos clave de phishing.
   - El panel analítico muestra puntuaciones en tiempo real para orientar la intervención del instructor.
3. **Laboratorio de análisis de correos**
   - A través de los simuladores del CyberRangeCZ, los/las trainees clasifican correos potencialmente maliciosos, verifican cabeceras y adjuntos en un entorno controlado.
   - Las acciones se registran y se vinculan con los objetivos del curso para su evaluación posterior.
4. **Cierre y reporte**
   - REP Practical Labs consolida los resultados del laboratorio y envía un resumen automático al Reporting Workspace.
   - El instructor revisa los hallazgos y coordina la retroalimentación grupal destacando aciertos y áreas de mejora.

## Ejercicios avanzados

### Campaña de spear phishing multicanal
- **Objetivo**: diseñar y ejecutar una campaña que combine correo electrónico, mensajería instantánea y llamadas simuladas para reforzar la detección de tácticas de spear phishing dirigidas.
- **Pasos clave**:
  1. En **REP Scheduler**, el instructor programa un bloque adicional que sincroniza los distintos canales y define los criterios de activación para cada grupo de trainees.
  2. Durante la actividad en **REP Live Session**, se liberan los mensajes según el guion temporal y se monitoriza la respuesta de los/las participantes en los canales colaborativos.
  3. Los resultados se documentan en **REP Practical Labs**, que registra evidencias de cada canal y permite comparar la eficacia de las contramedidas aplicadas.
  4. El **Reporting Workspace** consolida los indicadores de cada canal (tasa de clics, respuestas sospechosas, tiempos de reporte) para apoyar la discusión final.

### Cadena de respuesta colaborativa
- **Objetivo**: entrenar la coordinación entre roles técnicos y no técnicos ante una alerta de phishing escalada en la plataforma.
- **Pasos clave**:
  1. El instructor habilita en **REP Scheduler** una práctica secuencial que asigna tareas a cada rol (analista, communications lead, soporte legal) y define los disparadores de escalamiento.
  2. En **REP Live Session**, los/las trainees trabajan en tiempo real sobre el caso, utilizando los tableros compartidos y el chat para acordar decisiones y documentar acciones.
  3. **REP Practical Labs** captura los artefactos generados (formularios de notificación, tickets de soporte, análisis de evidencia) y verifica el cumplimiento de los pasos del playbook.
  4. El **Reporting Workspace** produce un informe de colaboración que destaca los hitos, tiempos de respuesta y dependencias críticas.

### Informe forense exprés
- **Objetivo**: elaborar un reporte condensado de análisis forense tras la detección de un phishing exitoso, sintetizando evidencias y recomendaciones.
- **Pasos clave**:
  1. A través de **REP Scheduler**, se despliega un módulo intensivo que incluye capturas de evidencias, logs y artefactos comprometidos para su revisión.
  2. En **REP Live Session**, el instructor guía un breve repaso de las evidencias críticas y aclara el alcance del informe que debe entregarse.
  3. Los/las trainees utilizan **REP Practical Labs** para procesar las evidencias, generar hallazgos preliminares y estructurar las secciones del informe.
  4. El informe final se carga en el **Reporting Workspace**, donde se valida contra una plantilla de incident response y se comparan las conclusiones entre equipos.

## Criterios de evaluación
- Configuración completa del curso en REP Scheduler con todos los materiales obligatorios.
- Tasa de respuestas correctas en los cuestionarios superior al umbral definido por el instructor.
- Cobertura del laboratorio: revisión de cabeceras, análisis de indicadores y verificación de adjuntos en los simuladores.
- Ejecución satisfactoria de los ejercicios avanzados, demostrando coordinación multicanal, colaboración entre roles y capacidad de síntesis forense según las pautas del Reporting Workspace.
- Entrega de un reporte final que sintetice riesgos detectados, hallazgos de los ejercicios avanzados y recomendaciones para mitigar campañas de phishing.

## Retroalimentación automática de la plataforma
- REP Quiz Engine muestra inmediatamente las respuestas correctas e incorrectas, incluyendo la explicación asociada a cada pregunta.
- REP Practical Labs asigna puntuaciones parciales por cada paso del análisis de correos (identificación del remitente, validación de enlaces y revisión de adjuntos) y genera alertas cuando falta documentar una evidencia.
- El Reporting Workspace emite un tablero resumen con indicadores de cumplimiento y un semáforo de riesgo por participante, que sirve como base para la retroalimentación personalizada del instructor.
- Para los ejercicios avanzados, REP Scheduler genera alertas sobre hitos no completados, REP Live Session ofrece registros de participación colaborativa y el Reporting Workspace añade paneles específicos que visualizan tiempos de respuesta, calidad de las entregas forenses y efectividad de la campaña multicanal.
