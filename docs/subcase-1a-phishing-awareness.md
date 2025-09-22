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

## Criterios de evaluación
- Configuración completa del curso en REP Scheduler con todos los materiales obligatorios.
- Tasa de respuestas correctas en los cuestionarios superior al umbral definido por el instructor.
- Cobertura del laboratorio: revisión de cabeceras, análisis de indicadores y verificación de adjuntos en los simuladores.
- Entrega de un reporte final que sintetice riesgos detectados y recomendaciones para mitigar campañas de phishing.

## Retroalimentación automática de la plataforma
- REP Quiz Engine muestra inmediatamente las respuestas correctas e incorrectas, incluyendo la explicación asociada a cada pregunta.
- REP Practical Labs asigna puntuaciones parciales por cada paso del análisis de correos (identificación del remitente, validación de enlaces y revisión de adjuntos) y genera alertas cuando falta documentar una evidencia.
- El Reporting Workspace emite un tablero resumen con indicadores de cumplimiento y un semáforo de riesgo por participante, que sirve como base para la retroalimentación personalizada del instructor.
