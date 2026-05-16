# Script que corre todas las métricas de evaluación del sistema
# Ejecutar con: python -m eval.run

import json
import httpx
import time
from pathlib import Path

# URL base del servidor, debe estar corriendo antes de ejecutar este script
BASE_URL = "http://127.0.0.1:8000/api/v1/api"

# Rutas a los datasets de evaluación
PROFILES_PATH = Path("eval/test_profiles.jsonl")
REVIEWS_PATH = Path("eval/test_reviews.jsonl")


def load_jsonl(path: Path) -> list[dict]:
    """Lee un archivo .jsonl y regresa una lista de diccionarios"""
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def eval_recommend(profiles: list[dict]) -> float:
    """
    Mide la cobertura del recomendador.
    Por cada perfil llama al endpoint /recommend y verifica que responde correctamente.
    Regresa el porcentaje de perfiles que obtuvieron respuesta exitosa.
    """
    print("\n--- Evaluando recomendador ---")
    exitosos = 0

    for i, profile in enumerate(profiles):
        try:
            response = httpx.post(
                f"{BASE_URL}/recommend",
                json={
                    "skin_type": profile["skin_type"],
                    "age": profile["age"],
                    "goal": profile["goal"],
                    "budget": profile["budget"],
                },
                timeout=30,
            )
            if response.status_code == 200:
                data = response.json()
                # Verificamos que regreso productos y rutina
                if data.get("products") and data.get("routine"):
                    exitosos += 1
                    print(f"  Perfil {i+1}: OK — {len(data['products'])} productos")
                else:
                    print(f"  Perfil {i+1}: FALLO — respuesta vacia")
            else:
                print(f"  Perfil {i+1}: ERROR {response.status_code}")
        except Exception as e:
            print(f"  Perfil {i+1}: EXCEPCION — {e}")

    cobertura = exitosos / len(profiles) * 100
    print(f"\nCobertura recomendador: {exitosos}/{len(profiles)} = {cobertura:.1f}%")
    return cobertura


def eval_sentiment(reviews: list[dict]) -> float:
    """
    Mide la precision del analizador de sentimiento.
    Manda todas las reseñas al endpoint /analyze-reviews y compara
    el sentimiento predominante contra las etiquetas reales.
    Regresa el porcentaje de precision.
    """
    print("\n--- Evaluando analizador de sentimiento ---")

    # Contamos cuantas reseñas son de cada tipo segun las etiquetas reales
    etiquetas = [r["sentiment"] for r in reviews]
    textos = [r["text"] for r in reviews]

    try:
        response = httpx.post(
            f"{BASE_URL}/analyze-reviews",
            json={"reviews": textos},
            timeout=60,
        )

        if response.status_code == 200:
            data = response.json()
            dist = data["sentiment_distribution"]
            temas = data["themes"]
            resumen = data["summary"]

            # Contamos etiquetas reales
            total = len(etiquetas)
            positivos_reales = etiquetas.count("positive") / total
            negativos_reales = etiquetas.count("negative") / total
            neutrales_reales = etiquetas.count("neutral") / total

            print(f"  Sentimiento real:      positive={positivos_reales:.2f} negative={negativos_reales:.2f} neutral={neutrales_reales:.2f}")
            print(f"  Sentimiento detectado: positive={dist.get('positive', 0):.2f} negative={dist.get('negative', 0):.2f} neutral={dist.get('neutral', 0):.2f}")
            print(f"  Temas detectados: {[t['theme'] for t in temas]}")
            print(f"  Resumen: {resumen[:100]}...")

            # Calculamos precision comparando el sentimiento predominante
            predominante_real = max(["positive", "negative", "neutral"], key=lambda x: etiquetas.count(x))
            predominante_detectado = max(dist, key=dist.get)

            precision = 100.0 if predominante_real == predominante_detectado else 0.0
            print(f"\nSentimiento predominante real: {predominante_real}")
            print(f"Sentimiento predominante detectado: {predominante_detectado}")
            print(f"Precision sentimiento: {precision:.1f}%")
            return precision
        else:
            print(f"  ERROR {response.status_code}")
            return 0.0
    except Exception as e:
        print(f"  EXCEPCION — {e}")
        return 0.0


def eval_latencia() -> float:
    """
    Mide la latencia del endpoint /chat con un mensaje simple.
    Regresa el tiempo en segundos.
    """
    print("\n--- Evaluando latencia ---")

    start = time.time()
    try:
        response = httpx.post(
            f"{BASE_URL}/chat",
            json={"session_id": "eval-latencia", "message": "hola"},
            timeout=30,
        )
        latencia = time.time() - start

        if response.status_code == 200:
            print(f"  Latencia: {latencia:.2f} segundos")
            if latencia <= 3:
                print("  Resultado: OK (menor a 3 segundos)")
            else:
                print("  Resultado: LENTO (mayor a 3 segundos)")
        else:
            print(f"  ERROR {response.status_code}")

        return latencia
    except Exception as e:
        print(f"  EXCEPCION — {e}")
        return 0.0


def main():
    print("=" * 50)
    print("EVALUACION DEL SISTEMA SKINCARE ASSISTANT")
    print("=" * 50)

    # Cargamos los datasets
    profiles = load_jsonl(PROFILES_PATH)
    reviews = load_jsonl(REVIEWS_PATH)

    print(f"\nDatasets cargados:")
    print(f"  Perfiles: {len(profiles)}")
    print(f"  Reseñas: {len(reviews)}")

    # Corremos las evaluaciones
    cobertura = eval_recommend(profiles)
    precision = eval_sentiment(reviews)
    latencia = eval_latencia()

    # Resumen final
    print("\n" + "=" * 50)
    print("RESUMEN FINAL")
    print("=" * 50)
    print(f"Cobertura recomendador: {cobertura:.1f}% (objetivo >= 70%)")
    print(f"Precision sentimiento:  {precision:.1f}% (objetivo >= 85%)")
    print(f"Latencia chat:          {latencia:.2f}s (objetivo <= 3s)")


if __name__ == "__main__":
    main()