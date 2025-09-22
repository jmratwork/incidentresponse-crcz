# CyberRangeCZ - Ejercicios prácticos

Este repositorio recopila únicamente los materiales necesarios para ejecutar los ejercicios prácticos de la iniciativa **CyberRangeCZ**. No incluye infraestructuras genéricas ni dependencias del laboratorio KYPO; todo el contenido está centrado en los flujos operativos actualmente validados para los subcasos 1a y 1d del diagrama de arquitectura.

## Alcance de los ejercicios

- **Subcaso 1a – Entrenamiento guiado por instructor**: describe la dinámica educativa combinando al instructor, la plataforma Random Education Platform (REP) y los/las participantes.
- **Subcaso 1d – Operación NG-SOC**: documenta cómo los componentes NG-SOC/NG-SIEM y NG-SOAR coordinan la respuesta automatizada apoyándose en el operador CICMS, CTI-SS y la biblioteca de playbooks/estándares (NVD/NIST, MITRE ATT&CK).

A continuación se resume el flujo detallado de cada subcaso para facilitar su reproducción durante las sesiones prácticas.

## Flujo del Subcaso 1a

1. **Preparación del instructor**  
   - El instructor revisa la guía del ejercicio y configura la sesión en la REP con los módulos correspondientes al tema del día.  
   - Se habilitan las herramientas colaborativas (chat, videoconferencia, pizarra digital) que acompañarán la sesión.
2. **Sesión en la Random Education Platform (REP)**  
   - El instructor inicia la transmisión del contenido y comparte los objetivos.  
   - La REP asigna automáticamente a cada participante un itinerario personalizado combinando teoría breve, escenarios simulados y recordatorios de buenas prácticas.
3. **Cuestionarios formativos para trainees**  
   - Los/las trainees completan cuestionarios interactivos en la REP para validar la comprensión inmediata.  
   - El instructor monitoriza en tiempo real los resultados y ofrece retroalimentación puntual.
4. **Pruebas prácticas evaluadas**  
   - La REP genera ejercicios prácticos supervisados (laboratorios virtuales o retos breves).  
   - Los resultados se registran y se consolidan en un reporte que el instructor revisa con el grupo durante la retroalimentación final.

## Flujo del Subcaso 1d

1. **Detección en NG-SOC/NG-SIEM**  
   - NG-SIEM recibe eventos desde las fuentes de telemetría del CyberRangeCZ y genera alertas priorizadas.  
   - El analista de NG-SOC valida la alerta y selecciona el playbook CACAO pertinente.
2. **Orquestación de playbooks CACAO**  
   - El orquestador NG-SOC invoca el NG-SOAR para ejecutar el playbook seleccionado.  
   - NG-SOAR coordina tareas automáticas (enriquecimiento, contención y notificación) respetando la secuencia definida en CACAO.
3. **Apoyo de sistemas transversales**
   - **CICMS Operator** centraliza la documentación del incidente y canaliza los reportes posteriores.
   - **CTI-SS** aporta inteligencia de amenazas y contexto adicional para la toma de decisiones.
   - **Biblioteca de playbooks y estándares (NVD/NIST, MITRE ATT&CK)** guía la selección de acciones de respuesta y recuperación.
4. **Cierre y retroalimentación**
   - NG-SOAR consolida los resultados y devuelve el estado final a NG-SOC/NG-SIEM.
   - CICMS Operator genera el reporte post-incidente y referencia las lecciones aprendidas en la biblioteca de playbooks.

## Archivos principales

- `training_linear.json`: lista los módulos de aprendizaje de los subcasos 1a y 1d, con actividades paso a paso y herramientas implicadas.
- `topology.yml`: describe los componentes del CyberRangeCZ relevantes para los ejercicios y su integración con las herramientas educativas y operativas.
- `docs/`: materiales de apoyo y guías complementarias.

## Licencia

El contenido se entrega con fines estrictamente educativos dentro del marco de CyberRangeCZ.
