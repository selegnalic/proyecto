# Skincare Assistant 

Sistema inteligente que analiza reseñas de productos de skincare y recomienda rutinas personalizadas según el tipo de piel, presupuesto y objetivos del usuario.

## ¿Qué hace?

- **Chatbot conversacional** — recolecta tu perfil (tipo de piel, edad, objetivo, presupuesto) y recomienda productos
- **Análisis de reseñas** — clasifica opiniones en positivas, negativas y neutras, detecta temas recurrentes y genera un resumen
- **Recomendaciones personalizadas** — sugiere productos y rutinas basadas en tu perfil

## Tecnologías

- **Backend**: FastAPI + LangGraph + LangChain
- **LLM**: OpenAI GPT-4o-mini
- **Base vectorial**: ChromaDB
- **Embeddings**: OpenAI text-embedding-3-small
- **Frontend**: React + Vite + Tailwind CSS
- **Dataset**: Sephora Products (Kaggle) — 2420 productos

## Instalación

```bash
git clone https://github.com/selegnalic/proyecto.git
cd proyecto
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración

```bash
cp .env.example .env
```

Edita el `.env` y agrega tu API key:

```
OPENAI_API_KEY=sk-...
```

## Cómo correrlo

```bash
uvicorn app.main:app --reload
```

Abre http://127.0.0.1:8000/docs para ver la documentación interactiva.

## Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/chat` | Chatbot conversacional con memoria |
| POST | `/api/recommend` | Recomendaciones por perfil |
| POST | `/api/analyze-reviews` | Análisis de reseñas |
| GET | `/api/health` | Estado de la API |

## Estructura del proyecto

```
proyecto/
├── app/
│   ├── agents/
│   │   ├── sales_agent.py    # LangGraph + memoria conversacional
│   │   └── review_agent.py   # Análisis de reseñas
│   ├── api/
│   │   ├── chat.py           # Endpoint chatbot
│   │   ├── recommend.py      # Endpoint recomendaciones
│   │   └── analyze.py        # Endpoint análisis
│   ├── core/
│   │   ├── config.py         # Configuración
│   │   └── llm.py            # Factory LLM
│   ├── rag/
│   │   ├── embeddings.py     # Factory embeddings
│   │   └── vectorstore.py    # ChromaDB
│   ├── data/
│   │   └── catalog.json      # 2420 productos de skincare
│   └── schemas/
│       └── chat.py           # Modelos Pydantic
├── frontend/                 # React + Vite
├── docs/                     # Documentación
├── eval/                     # Datasets de evaluación
└── .env.example
```

## Notas

- Los precios están en USD ya que el dataset es de Sephora USA
- No reemplaza la consulta con un dermatólogo
- Requiere API key de OpenAI