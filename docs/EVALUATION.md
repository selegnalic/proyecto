# Evaluación del Sistema

Este documento define cómo se valida la calidad del asistente de skincare y del analizador de reseñas.

## Métricas

### 1. Recall@k (recomendador)

**Qué mide:** dado un perfil de usuario etiquetado con un producto "correcto" por un experto, ¿aparece ese producto en el top-k de recomendaciones?

- **k = 5** para el MVP.
- **Umbral objetivo:** ≥ 70%.
- **Dataset:** `eval/test_profiles.jsonl` con 50 perfiles sintéticos generados a partir de combinaciones realistas de `skin_type × age × goal × budget`.

**Fórmula:**
```
recall@5 = (# perfiles donde producto_esperado ∈ top_5) / total_perfiles
```

### 2. Tasa de alucinación

**Qué mide:** porcentaje de respuestas donde el agente menciona productos que **no existen** en el catálogo.

- **Detección:** extraer nombres de producto de la respuesta con regex + matching exacto contra `CATALOG` en `app/data/catalog.py`.
- **Umbral objetivo:** ≤ 2%.
- **Muestra:** 100 conversaciones simuladas.

### 3. Latencia p95

**Qué mide:** tiempo de respuesta del endpoint `/api/chat` bajo carga normal.

- **Umbral objetivo:** ≤ 3 segundos.
- **Medición:** `httpx` con 20 requests concurrentes, percentil 95.

### 4. Calidad de justificación (LLM-as-judge)

**Qué mide:** coherencia entre la justificación ("por qué este producto") y el perfil del cliente.

- **Modelo juez:** GPT-4 (distinto al LLM que genera la respuesta).
- **Escala:** 1 (incoherente) — 5 (excelente ajuste).
- **Prompt del juez:**
  > "Dado este perfil de cliente {profile} y esta recomendación {response}, evalúa en escala 1-5 qué tan bien se ajusta la recomendación al perfil. Justifica tu puntuación."
- **Muestra:** 50 respuestas por iteración del prompt.
- **Umbral objetivo:** media ≥ 4.0.

### 5. Cobertura de onboarding

**Qué mide:** porcentaje de sesiones donde el agente recolecta los 4 datos (`skin_type`, `age`, `goal`, `budget`) sin dejar huecos.

- **Método:** revisión manual de 20 conversaciones completas.
- **Umbral objetivo:** ≥ 90%.

### 6. Clasificación de sentimiento (analizador de reseñas)

**Qué mide:** accuracy de la clasificación positive/negative/neutral.

- **Dataset:** `eval/test_reviews.jsonl` con 100 reseñas etiquetadas.
- **Umbral objetivo:** ≥ 85% accuracy.

## Estructura de los datasets de evaluación

### `eval/test_profiles.jsonl`

```jsonl
{"skin_type": "seca", "age": 32, "goal": "hidratación", "budget": 500, "expected_product_id": "p008"}
{"skin_type": "grasa", "age": 24, "goal": "control de acné", "budget": 800, "expected_product_id": "p016"}
```

### `eval/test_reviews.jsonl`

```jsonl
{"text": "Excelente hidratación, mi piel mejoró en una semana", "sentiment": "positive", "themes": ["hidratación", "efectividad"]}
{"text": "Caro para la cantidad que viene", "sentiment": "negative", "themes": ["precio"]}
```

## Ejecución

```bash
# Pendiente: crear eval/run.py que corre todas las métricas
python -m eval.run --profiles eval/test_profiles.jsonl --reviews eval/test_reviews.jsonl
```

## Frecuencia

- **Por PR:** smoke test (10 perfiles, 10 reseñas).
- **Por release:** suite completa.
- **Manual:** cada vez que se cambien prompts o se suba de modelo.
