from __future__ import annotations

from typing import Optional

import chromadb
import numpy as np
from fastembed import TextEmbedding

from . import config
from .config import CHROMA_PERSIST_DIR, EMBEDDING_MODEL_NAME
from .graphrag.neo4j_store import Neo4jGraphStore


RERANKER_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class FastEmbedder:
    """Adapter that preserves the encode() interface used by the application."""

    def __init__(self, model_name: str) -> None:
        self._model = TextEmbedding(
            model_name=model_name,
            threads=2,
        )

    def encode(
        self,
        sentences: str | list[str],
        normalize_embeddings: bool = True,
        show_progress_bar: bool = False,
    ) -> np.ndarray:
        del show_progress_bar

        single_input = isinstance(sentences, str)
        texts = [sentences] if single_input else list(sentences)

        if not texts:
            if single_input:
                return np.empty((0,), dtype=np.float32)
            return np.empty((0, 0), dtype=np.float32)

        vectors = list(self._model.embed(texts, batch_size=16))
        embeddings = np.asarray(vectors, dtype=np.float32)

        if normalize_embeddings:
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            embeddings = embeddings / np.maximum(norms, 1e-12)

        return embeddings[0] if single_input else embeddings


_store: Optional[Neo4jGraphStore] = None
_embedder: Optional[FastEmbedder] = None
_reranker = None
_chroma_client = None


def get_store() -> Neo4jGraphStore:
    global _store

    if _store is None:
        _store = Neo4jGraphStore(
            uri=config.require_env("NEO4J_URI"),
            user=config.require_env("NEO4J_USER"),
            password=config.require_env("NEO4J_PASSWORD"),
        )
        _store.ensure_schema()

    return _store


def get_embedder() -> FastEmbedder:
    global _embedder

    if _embedder is None:
        _embedder = FastEmbedder(EMBEDDING_MODEL_NAME)

    return _embedder


def get_reranker():
    global _reranker

    if _reranker is None:
        from sentence_transformers import CrossEncoder

        _reranker = CrossEncoder(RERANKER_MODEL_NAME)

    return _reranker


def get_chroma_collection(collection_name: str):
    global _chroma_client

    if _chroma_client is None:
        _chroma_client = chromadb.PersistentClient(
            path=CHROMA_PERSIST_DIR
        )

    return _chroma_client.get_or_create_collection(
        name=collection_name
    )


def preload_models(include_neo4j: bool = True) -> None:
    get_embedder()
    get_reranker()

    if include_neo4j:
        get_store()