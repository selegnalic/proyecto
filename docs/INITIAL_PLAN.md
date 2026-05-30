# Propuestas de Proyectos de Ingeniería en IA

## 1. Analizador Inteligente de Opiniones de Negocios

### Descripción

Este proyecto consiste en desarrollar un sistema capaz de analizar grandes volúmenes de comentarios de clientes (por ejemplo, reseñas de productos o servicios) para identificar los temas más relevantes y clasificar las opiniones en positivas y negativas.

### Objetivo

El objetivo principal es mejorar la atención al cliente mediante el entendimiento de:

- **Aspectos positivos:** identificar qué es lo que más valoran los clientes.
- **Aspectos negativos:** detectar áreas de oportunidad para mejorar el servicio o producto.

### Funcionalidades principales

- Clasificación de comentarios en:
  - Positivos
  - Negativos
- Detección de temas recurrentes (precio, calidad, servicio, etc.)
- Resumen automático de opiniones por categoría
- Sistema de preguntas y respuestas sobre los comentarios (QA)

---

## 2. Asistente de Ventas Inteligente

### Descripción

Este proyecto consiste en crear un asistente virtual que recomienda productos personalizados según las necesidades específicas del cliente, enfocado en un nicho como el cuidado de la piel.

### Objetivo

Brindar recomendaciones personalizadas que ayuden al cliente a elegir productos adecuados según:

- Tipo de piel (seca, grasa, mixta)
- Presupuesto
- Objetivos (hidratación, anti-acné, anti-edad)
- Rutina completa de cuidado

### Funcionalidades principales

- Recomendación de productos dentro de un rango de presupuesto
- Generación de rutinas personalizadas
- Respuestas a preguntas del cliente
- Búsqueda inteligente en catálogo de productos (RAG)

### Ejemplo de uso

Un cliente proporciona la siguiente información:

- **Tipo de piel:** seca
- **Presupuesto:** $500
- **Objetivo:** hidratación

El sistema responde con:

- Lista de productos recomendados
- Rutina paso a paso
- Justificación de las recomendaciones

---

## Resumen Ejecutivo

### ¿Qué es?

Este proyecto consiste en desarrollar un sistema capaz de analizar grandes volúmenes de comentarios de clientes, reseñas de productos o servicios para identificar los temas más relevantes y clasificar las opiniones en positivas y negativas, además de recomendar productos personalizados según las necesidades específicas del cliente, enfocado en un nicho como el cuidado de la piel.

### ¿Por qué importa?

Debido a tanta información con tantos productos puede ser agobiante encontrar un producto que sea accesible y que sea de acuerdo a las necesidades de tu piel. No pretende reemplazar a un dermatólogo, pero sí orientar de acuerdo al tipo de piel y relacionar con lo que prometen los productos.

### ¿Cómo funciona?

El cliente interactúa con un robot, donde contesta preguntas básicas: tipo de piel, qué es lo que quiere mejorar (líneas de expresión, manchas, etc.), edad y presupuesto.

### ¿Qué valor aporta?

Evitar buscar en diferentes páginas y perfiles de influencer, teniendo información más resumida con las opciones disponibles de acuerdo a las necesidades del cliente.

---

## Objetivos del Proyecto

Desarrollar un sistema inteligente que permita analizar opiniones de clientes para identificar aspectos positivos y áreas de mejora en productos o servicios, así como detectar tendencias de consumo (productos más y menos vendidos). Adicionalmente, el sistema ofrecerá recomendaciones personalizadas de productos y rutinas de cuidado de la piel, considerando el tipo de piel, presupuesto y objetivos específicos del usuario, con el fin de mejorar la experiencia del cliente y optimizar la toma de decisiones.

---

## Matriz de Características e Historias de Usuario

### Características

| Característica | Descripción |
| --- | --- |
| Clasificación de comentarios | Como tienda que vende productos de cuidado de la piel, quiero conocer cómo percibe el cliente nuestro servicio. |
| Detección de temas recurrentes (precio, calidad, servicio) | Conocer los temas más mencionados para detectar áreas de oportunidad y saber qué estamos haciendo bien. |
| Resumen automático de opiniones por categoría | Es importante tener el resumen de opiniones para una toma de decisiones rápida. |
| Recomendación de productos dentro de un rango de presupuesto (respuestas a preguntas del cliente) | Del lado del cliente, hay una amplia gama de productos, lo cual puede ser agobiante para elegir el producto adecuado y con un presupuesto limitado. El objetivo es tener recomendaciones personalizadas. |
| Búsqueda inteligente en el catálogo de productos | Después de tener la información necesaria del cliente, el sistema buscará dentro de sus productos disponibles los que satisfagan las necesidades del cliente y que estén dentro del presupuesto. |

### Historias de Usuario

- **Como cliente**, interactúo con un robot donde me hace preguntas generales sobre el tipo de piel (mixta, grasa, seca), mi edad, si quiero algo muy específico (por ejemplo, un protector solar: no todos son para cualquier tipo de piel ni tienen el mismo precio), o si quiero una rutina completa para noche o día, y el presupuesto del que dispongo. Con base en esos datos, el robot me dará un resumen con los productos disponibles y los beneficios de cada uno, para que pueda elegir el que mejor me convenza.
- **Como dueño de la tienda**, quiero identificar rápidamente los principales problemas reportados por los clientes.

---

## Arquitectura Técnica del Sistema

### 1. Componentes Principales

#### 1.1 Cliente (Frontend o Usuario)

Es la interfaz desde la cual el usuario interactúa con el sistema. Puede ser un chatbot donde el usuario interactúa haciendo una serie de preguntas para recomendarle una rutina. Al obtener su rutina, se le pregunta si ya ha utilizado algún otro producto de cuidado para conocer su opinión; si no, se le enviará un formulario después de cierto tiempo (1 mes aprox.) para conocer su opinión y que evalúe también el servicio.

**Funciones:**

- Enviar consultas o datos
- Recibir respuestas del sistema

#### 1.2 API Backend (FastAPI)

Es el núcleo del sistema que gestiona la lógica de negocio.

**Funciones:**

- Recibir solicitudes del usuario
- Procesar datos de entrada
- Llamar a los chains de LangChain
- Devolver respuestas

#### 1.3 Motor de IA (LangChain)

Orquesta la interacción con el modelo de lenguaje.

**Componentes:**

- **Prompts** (definen el comportamiento del modelo)
- **Chains** (flujo de procesamiento)
- **Memory** (manejo de contexto, opcional)

#### 1.4 Modelo de Lenguaje (LLM)

Encargado de generar respuestas inteligentes basadas en el contexto.

**Funciones:**

- Clasificación de texto
- Generación de respuestas
- Resumen de información

#### 1.5 Base de Datos Vectorial

Almacena embeddings de los datos (comentarios o productos).

**Funciones:**

- Búsqueda semántica
- Recuperación de información relevante (RAG)

#### 1.6 Pipeline de Procesamiento (RAG)

Permite combinar búsqueda de información con generación de texto.

**Flujo:**

1. Entrada del usuario
2. Conversión a embedding
3. Búsqueda en base vectorial
4. Recuperación de información relevante
5. Generación de respuesta con LLM

### 2. Flujo de Funcionamiento

1. El usuario envía una consulta al sistema.
2. FastAPI recibe la solicitud.
3. LangChain procesa la entrada utilizando prompts y chains.
4. Si es necesario, se realiza una búsqueda en la base de datos vectorial (RAG).
5. El modelo de lenguaje genera una respuesta.
6. La respuesta es enviada de vuelta al usuario.

### 3. Tecnologías Utilizadas

#### Backend
- **Python 3.11+**
- **FastAPI** — servidor HTTP, validación Pydantic nativa
- **LangGraph** — orquestación del agente conversacional con memoria persistente (`MemorySaver` + `thread_id`)
- **LangChain** — sólo para loaders/retrievers del pipeline RAG (no para memoria)
- **OpenAI SDK** — LLM (`gpt-4o-mini` por defecto) y embeddings (`text-embedding-3-small`)
- **ChromaDB** — base vectorial embebida, persistencia en disco
- **sentence-transformers** — fallback de embeddings locales (`BAAI/bge-m3`)

#### Frontend
- **React 18 + TypeScript** sobre **Vite**
- **Tailwind CSS** para estilos
- Persistencia de `session_id` en `localStorage`

#### Decisión: LangGraph sobre LangChain memory o Pydantic AI

| Framework | Decisión | Razón |
|---|---|---|
| **LangGraph** | ✅ Elegido | Memoria nativa vía `MemorySaver` + `thread_id`. Estado explícito como "blackboard". Estándar 2026 para chatbots stateful con flujos de onboarding secuenciales. |
| LangChain memory (solo) | ❌ | `ConversationBufferMemory` es pattern deprecado; la propia LangChain recomienda migrar a LangGraph. |
| Pydantic AI | ❌ | Excelente para agentes con tool-calling, pero su modelo de memoria es menos expresivo para flujos secuenciales tipo formulario. |

#### Decisión: Modelo de embeddings

Estrategia dual, config-switchable vía `EMBED_PROVIDER` env var:

| Modelo | Dims | Costo | Español | Uso |
|---|---|---|---|---|
| **`text-embedding-3-small`** (OpenAI) | 1536 | **$0.02 / 1M tokens** | ✅ | **Default** para MVP — costo de indexar catálogo de 10K productos < $1 |
| `text-embedding-3-large` (OpenAI) | 3072 | $0.13 / 1M tokens (6.5× más caro) | ✅ | Escalar sólo si recall@k insuficiente (+4pp en MTEB) |
| `BAAI/bge-m3` (HuggingFace, local) | 1024 | $0 | ✅ 100+ idiomas | **Fallback sin API key** — `EMBED_PROVIDER=hf` |
| `intfloat/multilingual-e5-large` (HF) | 1024 | $0 | ✅ | Alternativa gratis |
| `all-MiniLM-L6-v2` | 384 | $0 | ❌ solo EN | Descartado (catálogo en español) |

### 4. Diagrama Conceptual

```
React UI (Vite) ──HTTP──► FastAPI ──► LangGraph (MemorySaver)
                                          ↓
                                        LLM (OpenAI)
                                          ↓
                                   RAG: Chroma + embeddings
                                          ↓
                                      Respuesta
```

---

## Fuentes de Datos

### Datasets públicos recomendados (con licencia)

| Dataset | Contenido | URL | Uso propuesto |
|---|---|---|---|
| **Sephora Products and Skincare Reviews** (Kaggle, nadyinky) | Productos + reseñas con `product_id`, `rating`, `review_text` | https://www.kaggle.com/datasets/nadyinky/sephora-products-and-skincare-reviews | ✅ Catálogo principal + corpus para analizador de reseñas |
| **Amazon Beauty Products con ingredientes (47K)** | Ingredientes completos, precios, descripciones, disponibilidad | https://crawlfeeds.com/datasets/amazon-beauty-products-dataset-with-ingredients-47k-records | Complementario (revisar licencia específica antes de uso) |
| **Amazon Skincare Products** (Kaggle) | Categorías (moisturizer, primer, cream, etc.) | https://www.kaggle.com/datasets/namantrisoliya/amazon-skincare-products | Complementario para cobertura de categorías |

### APIs oficiales: NO existen

**Sephora, Ulta, Mercado Libre y Amazon no exponen APIs públicas** para sus catálogos de skincare.

Los servicios listados como "Sephora API" (RapidAPI, Apify, Oxylabs, Retailed.io) son **scrapers comerciales de terceros** — mismo riesgo legal que hacer scraping directo, más un costo mensual. **Se descartan.**

### Estrategia para el MVP

1. **Fase MVP (actual):** catálogo sintético de ~30 productos generado manualmente en `app/data/catalog.py` para demostrar el flujo end-to-end sin bloqueo por datos.
2. **Fase ampliación:** reemplazar catálogo sintético con el dataset de Sephora de Kaggle (descarga manual con licencia CC0 / público).
3. **Fase operación:** la base crece con productos introducidos por el dueño de la tienda vía endpoint admin (fuera de alcance del MVP).

### Lo que NO haremos

- ❌ Scraping de Amazon, Mercado Libre, Sephora.com (viola ToS — ver Riesgo 7).
- ❌ Contratar scrapers comerciales de terceros (mismo problema legal + costo).

---

## API Endpoints

Todos los endpoints están bajo el prefijo `/api`. CORS habilitado para `http://localhost:5173` (Vite dev server).

### `POST /api/chat` — Conversación principal

Orquestado por LangGraph. Mantiene estado por `session_id` (usado como `thread_id` en `MemorySaver`).

**Request:**
```json
{
  "session_id": "uuid-v4",
  "message": "Tengo piel seca y quiero una rutina de noche"
}
```

**Response:**
```json
{
  "reply": "¿Qué edad tienes y cuál es tu presupuesto aproximado?",
  "state": {
    "skin_type": "seca",
    "goal": "rutina de noche",
    "age": null,
    "budget": null,
    "ready_to_recommend": false
  }
}
```

Cuando `state.ready_to_recommend` es `true`, la respuesta incluye los productos recomendados.

### `POST /api/recommend` — Recomendación directa (sin chat)

Para clientes que ya conocen sus datos y quieren saltar el onboarding.

**Request:**
```json
{
  "skin_type": "seca",
  "age": 32,
  "budget": 500,
  "goal": "hidratación"
}
```

**Response:**
```json
{
  "products": [
    {"name": "...", "price": 250, "rationale": "..."}
  ],
  "routine": ["Paso 1: ...", "Paso 2: ..."]
}
```

### `POST /api/analyze-reviews` — Analizador de opiniones

**Request:**
```json
{
  "reviews": ["Excelente producto...", "No me gustó la textura..."]
}
```

**Response:**
```json
{
  "sentiment_distribution": {"positive": 0.6, "negative": 0.3, "neutral": 0.1},
  "themes": [{"theme": "precio", "mentions": 12}, {"theme": "textura", "mentions": 8}],
  "summary": "La mayoría de clientes valora la eficacia pero..."
}
```

### `GET /api/health` — Health check (existente)

```json
{"status": "ok"}
```

---

## Evaluación del Sistema

### Métricas cuantitativas

| Métrica | Cómo se mide | Umbral objetivo MVP |
|---|---|---|
| **Recall@5** | Sobre test set de ~50 perfiles de usuario etiquetados con productos "correctos", ¿el producto aparece en el top-5 de recomendaciones? | ≥ 70% |
| **Tasa de alucinación** | % de respuestas donde el producto mencionado **no existe** en el catálogo (detectado con matching exacto de nombre o ID) | ≤ 2% |
| **Latencia p95** | Tiempo de respuesta del endpoint `/api/chat` | ≤ 3s |

### Métricas cualitativas

| Métrica | Método |
|---|---|
| **Calidad de justificación** | LLM-as-judge: GPT-4 evalúa en escala 1-5 si la justificación ("por qué este producto") es coherente con el perfil del cliente. Muestra de 50 respuestas por iteración. |
| **Cobertura de onboarding** | % de sesiones donde el agente recolecta los 4 datos (tipo de piel, edad, objetivo, presupuesto) sin dejar huecos. Revisión manual de 20 conversaciones. |

### Set de evaluación

- `eval/test_profiles.jsonl` — 50 perfiles sintéticos con `skin_type`, `age`, `goal`, `budget` + producto esperado.
- `eval/test_reviews.jsonl` — 100 reseñas etiquetadas (sentiment, tema principal) para el analizador.

Ver detalles en `docs/EVALUATION.md`.

---

## Roadmap de Desarrollo

### Fase 1: Definición del Proyecto

**Objetivo:** Establecer el alcance y requerimientos del sistema.

**Actividades:**

- Definir el problema a resolver
- Identificar usuarios y casos de uso
- Definir funcionalidades principales
- Seleccionar tecnologías (LangChain, FastAPI, etc.)

### Fase 2: Recolección y Preparación de Datos

**Objetivo:** Obtener y preparar los datos necesarios para el sistema.

**Actividades:**

- Buscar datasets (por ejemplo, reseñas de productos)
- Limpieza de datos (eliminar ruido, duplicados)
- Estructuración de la información
- Exploración inicial de los datos

### Fase 3: Implementación de Embeddings y Base Vectorial

**Objetivo:** Preparar el sistema para búsquedas semánticas.

**Actividades:**

- Generar embeddings de los textos
- Almacenar embeddings en una base de datos vectorial
- Validar búsquedas semánticas básicas

### Fase 4: Desarrollo del Sistema RAG

**Objetivo:** Integrar recuperación de información con generación de respuestas.

**Actividades:**

- Implementar pipeline de Retrieval-Augmented Generation (RAG)
- Configurar prompts para preguntas y respuestas
- Probar consultas sobre los datos

### Fase 5: Desarrollo de Chains y Lógica de Negocio

**Objetivo:** Construir la lógica principal del sistema.

**Actividades:**

- Crear chains (clasificación, resumen, QA)
- Implementar flujos de procesamiento
- Integrar memoria (opcional)

### Fase 6: Desarrollo del Backend (FastAPI)

**Objetivo:** Exponer el sistema mediante una API.

**Actividades:**

- Crear endpoints (consultas, análisis, recomendaciones)
- Integrar LangChain con FastAPI
- Manejo de errores y validaciones

### Fase 7: Evaluación del Sistema

**Objetivo:** Validar la calidad del sistema.

**Actividades:**

- Evaluar respuestas del modelo
- Medir precisión (si aplica)
- Revisión manual de resultados
- Ajuste de prompts
- Testing (API endpoints)

### Fase 8: Optimización y Mejora

**Objetivo:** Mejorar rendimiento y calidad.

**Actividades:**

- Optimizar prompts
- Ajustar parámetros del modelo
- Implementar caching o mejoras de velocidad
- Refinar resultados

### Fase 9: Documentación y Presentación

**Objetivo:** Preparar el proyecto para entrega.

**Actividades:**

- Documentar arquitectura técnica
- Crear README del proyecto
- Preparar ejemplos de uso
- Generar conclusiones y aprendizajes

### Fase 10: Despliegue (Opcional)

**Objetivo:** Hacer el sistema accesible.

**Actividades:**

- Desplegar API en la nube
- Configurar entorno de producción
- Pruebas finales

---

## Plan de Gestión de Riesgos (Business Oriented)

### Riesgo 1: Baja calidad de datos

- **Descripción:** Los datos (reseñas o productos) pueden estar incompletos, duplicados o contener ruido.
- **Impacto:** Resultados poco confiables, mala experiencia del usuario.
- **Probabilidad:** Alta
- **Mitigación:**
  - Limpieza y validación de datos
  - Uso de datasets confiables
  - Procesamiento previo (preprocessing)

### Riesgo 2: Respuestas incorrectas del modelo

- **Descripción:** El modelo puede generar información incorrecta o poco precisa.
- **Impacto:** Pérdida de confianza del usuario, decisiones erróneas.
- **Probabilidad:** Media
- **Mitigación:**
  - Uso de RAG para grounding de información
  - Validación de respuestas
  - Prompts bien diseñados

### Riesgo 3: Costos elevados de uso de API

- **Descripción:** El uso intensivo de modelos de lenguaje puede generar costos altos.
- **Impacto:** Afectación al presupuesto del proyecto.
- **Probabilidad:** Media
- **Mitigación:**
  - Optimización de llamadas al modelo
  - Uso de caché
  - Evaluación de modelos alternativos

### Riesgo 4: Problemas de rendimiento (latencia)

- **Descripción:** El sistema puede responder lentamente debido al procesamiento de IA.
- **Impacto:** Mala experiencia del usuario.
- **Probabilidad:** Media
- **Mitigación:**
  - Optimización de consultas
  - Uso eficiente de embeddings
  - Implementación de almacenamiento en caché

### Riesgo 5: Seguridad y manejo de datos sensibles

- **Descripción:** Exposición de información sensible (por ejemplo, API keys o datos de usuarios).
- **Impacto:** Riesgos legales y reputacionales.
- **Probabilidad:** Media
- **Mitigación:**
  - Uso de archivos `.env`
  - Implementación de `.gitignore`
  - Buenas prácticas de seguridad

### Riesgo 6: Mala interpretación de necesidades del usuario

- **Descripción:** El sistema puede no entender correctamente las solicitudes del usuario.
- **Impacto:** Respuestas irrelevantes o incorrectas.
- **Probabilidad:** Media
- **Mitigación:**
  - Mejora continua de prompts
  - Iteración con feedback de usuarios
  - Pruebas constantes

### Riesgo 7: Legal — scraping de marketplaces

- **Descripción:** Términos de servicio de Amazon, Mercado Libre, Sephora y similares **prohíben explícitamente** el scraping automatizado de sus catálogos y reseñas.
- **Impacto:** Riesgo de cease-and-desist, bloqueo de IPs, responsabilidad legal.
- **Probabilidad:** Alta si se ignora.
- **Mitigación:**
  - No scrapear Amazon/ML/Sephora directamente.
  - No contratar scrapers de terceros (RapidAPI/Apify/Oxylabs) — trasladan el mismo riesgo.
  - Usar datasets públicos con licencia (Kaggle CC0).
  - Generar catálogo sintético para MVP.
  - Si en producción se requiere catálogo real: acuerdo comercial directo con la tienda cliente (ella es dueña de sus datos).

---

## Interfaz UI

### Campo de Entrada

Permite al usuario ingresar texto, como:

- Preguntas sobre opiniones
- Solicitudes de recomendación
- Descripción de necesidades (tipo de piel, presupuesto, etc.)

**Ejemplo:**

> "Quiero una rutina para piel seca con presupuesto de $500"

### Botón de Envío

Permite enviar la solicitud al sistema para su procesamiento.

### Área de Resultados

Muestra la respuesta generada por el sistema, que puede incluir:

- Recomendaciones de productos
- Resumen de opiniones
- Clasificación de comentarios
- Respuestas a preguntas específicas

### Historial de Conversación

Permite visualizar interacciones previas para mantener contexto.

### Flujo de Interacción

1. El usuario ingresa una consulta en el campo de texto.
2. Presiona el botón de envío.
3. La solicitud se envía al backend (FastAPI).
4. El sistema procesa la información usando IA (LangChain + RAG).
5. La respuesta se muestra en el área de resultados.

### Tipo de Interfaz

**Chatbot conversacional**
