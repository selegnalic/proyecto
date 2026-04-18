"""Wrapper de ChromaDB sobre el catálogo de productos."""
from functools import lru_cache
from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.core.config import settings
from app.data.catalog import get_catalog
from app.rag.embeddings import get_embeddings

COLLECTION = "skincare_catalog"


def _product_to_document(p) -> Document:
    text = (
        f"{p.name} — {p.brand}\n"
        f"Precio: ${p.price}\n"
        f"Tipos de piel: {', '.join(p.skin_types)}\n"
        f"Indicado para: {', '.join(p.concerns)}\n"
        f"Descripción: {p.description}"
    )
    return Document(
        page_content=text,
        metadata={
            "id": p.id,
            "name": p.name,
            "brand": p.brand,
            "price": p.price,
            "skin_types": ",".join(p.skin_types),
            "concerns": ",".join(p.concerns),
        },
    )


@lru_cache(maxsize=1)
def get_vectorstore() -> Chroma:
    store = Chroma(
        collection_name=COLLECTION,
        embedding_function=get_embeddings(),
        persist_directory=settings.CHROMA_PERSIST_DIR,
    )

    if store._collection.count() == 0:
        docs = [_product_to_document(p) for p in get_catalog()]
        store.add_documents(docs)

    return store


def search_catalog(query: str, k: int = 5, budget: float | None = None) -> list[dict]:
    store = get_vectorstore()
    results = store.similarity_search(query, k=k * 3 if budget else k)

    hits = []
    for doc in results:
        price = doc.metadata.get("price", 0)
        if budget is not None and price > budget:
            continue
        hits.append({
            "id": doc.metadata["id"],
            "name": doc.metadata["name"],
            "brand": doc.metadata["brand"],
            "price": price,
            "description": doc.page_content,
        })
        if len(hits) >= k:
            break

    return hits
