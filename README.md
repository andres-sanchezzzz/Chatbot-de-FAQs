# Chatbot de FAQs

## Descripción
Este proyecto implementa un chatbot de preguntas frecuentes (FAQs) enfocado en temas de nómina y contratación, utilizando una base de conocimiento estructurada, guardrails de alcance y modelos de lenguaje (LLM) de forma controlada.

El objetivo es demostrar una arquitectura GenAI gobernada, evitando alucinaciones, controlando fuentes y garantizando trazabilidad en las respuestas.

## Arquitectura General

Usuario
  ↓
Interfaz (Streamlit)
  ↓
Retriever (KB + RapidFuzz)
  ↓
Guardrails (alcance, tono, seguridad)
  ↓
KB (FAQs) y Web Search (Google CSE) Dominios oficiales

  ↓
LLM (solo reformulación / resumen)
  ↓
Respuesta + Fuente

## Base de Conocimiento (KB)

- Fuente: archivo Excel con FAQs oficiales.
- Columnas:
  - Segmento/categoria de pregunta
  - pregunta
  - respuesta
- La KB se carga y normaliza en memoria al iniciar la aplicación.
- Es la única fuente de verdad para respuestas directas.

Archivo principal:
- `src/kb_loader.py`

## Retrieval (Búsqueda en KB)

- Se utiliza RapidFuzz para fuzzy matching.
- Parámetros configurables:
  - top-k: número de candidatos evaluados
  - threshold: puntaje mínimo para considerar una pregunta en alcance
- Si no se supera el umbral, la pregunta se considera fuera de alcance.

Archivo principal:
- `src/retriever.py`

## Guardrails (Gobernanza)

El módulo de guardrails centraliza las reglas de control del sistema:

- Determina si una pregunta está dentro del alcance permitido.
- Bloquea solicitudes sensibles.
- Define el tono de la respuesta (neutral, directo, empático).
- Decide cuándo habilitar búsqueda web.
- Evita que el LLM responda sin autorización explícita.

Archivo principal:
- `src/guardrails.py`

## Búsqueda Web Controlada

Cuando la pregunta no está cubierta por la KB y corresponde a temas normativos o legales, el sistema habilita una búsqueda web controlada usando Google Custom Search API.

Características:
- Restricción a dominios oficiales (ej. mintrabajo.gov.co).
- Sin scraping de buscadores.
- Fuentes verificables y auditables.

Archivo principal:
- `src/web_search.py`

## Uso del LLM

El modelo de lenguaje no es la fuente de verdad.

Se utiliza únicamente para:
- Reformular respuestas oficiales de la KB.
- Resumir contenido obtenido de fuentes web oficiales.

Medidas de control:
- Prompt cerrado.
- Baja temperatura.
- Inclusión obligatoria de la fuente.
- Ejecución solo si los guardrails lo permiten.

Archivo principal:
- `src/llm.py`

## Interfaz de Usuario

- Implementada con Streamlit.
- Funcionalidades:
  - Chat interactivo.
  - Memoria de corto plazo por sesión.
  - Reinicio de conversación.
- Diseñada como prueba de concepto (POC).

Archivo principal:
- `app.py`

## Variables de Entorno

En archivo `.env` en la raíz del proyecto:

## Ejecución del Proyecto

### Instalar dependencias

```pip install -r requirements.txt```

### Ejecutar la aplicacion

```streamlit run app.py```

## Pruebas Sugeridas

- Pregunta cubierta por KB:

"¿Cuándo pagan la nómina?"

- Pregunta fuera de alcance:

"¿Cuál es el salario de un compañero?"

- Pregunta legal (búsqueda web):

"¿Es legal un despido sin justa causa?"

## Decisiones de Diseño

- No se utiliza scraping de buscadores debido a bloqueos y captchas.
- Se emplean APIs oficiales para búsqueda web.
- La KB es la fuente primaria de información.
- Los guardrails gobiernan el acceso al LLM.
- Separación clara de responsabilidades entre componentes.

## Trabajo a Futuro

- Cache de resultados web.
-Logging persistente.
- Control por roles de usuario.
-Métricas de precisión del retriever.
- Integración con Azure OpenAI o Bing Search.

## Nota Final

Este proyecto prioriza seguridad, gobernanza y explicabilidad sobre complejidad innecesaria, alineándose con buenas prácticas de implementación de sistemas GenAI en entornos empresariales.
