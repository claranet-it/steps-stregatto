import re
import os
import string
import json
from typing import List, Any
from itertools import combinations
from sklearn.feature_extraction.text import CountVectorizer
from langchain_core.embeddings import Embeddings
from langchain_community.embeddings import BedrockEmbeddings
import httpx


class DumbEmbedder(Embeddings):
    """Default Dumb Embedder.

    This is the default embedder used for testing purposes
    and to replace official embedders when they are not available.

    Notes
    -----
    This class relies on the `CountVectorizer`[1]_ offered by Scikit-learn.
    This embedder uses a naive approach to extract features from a text and build an embedding vector.
    Namely, it looks for pairs of characters in text starting form a vocabulary with all possible pairs of
    printable characters, digits excluded.
    """

    def __init__(self):
        # Get all printable characters numbers excluded and make everything lowercase
        chars = [p.lower() for p in string.printable[10:]]

        # Make the vocabulary with all possible combinations of 2 characters
        voc = []
        for k in combinations(chars, 2):
            voc.append(f"{k[0]}{k[1]}")
        voc = sorted(set(voc))

        # Naive embedder that counts occurrences of couple of characters in text
        self.embedder = CountVectorizer(
            vocabulary=voc, analyzer=lambda s: re.findall("..", s), binary=True
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of text and returns the embedding vectors that are lists of floats."""
        return self.embedder.transform(texts).astype(float).todense().tolist()

    def embed_query(self, text: str) -> List[float]:
        """Embed a string of text and returns the embedding vector as a list of floats."""
        return self.embed_documents([text])[0]


class CustomOpenAIEmbeddings(Embeddings):
    """Use LLAMA2 as embedder by calling a self-hosted lama-cpp-python instance."""

    def __init__(self, url):
        self.url = os.path.join(url, "v1/embeddings")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        payload = json.dumps({"input": texts})
        ret = httpx.post(self.url, data=payload, timeout=None)
        ret.raise_for_status()
        return [e["embedding"] for e in ret.json()["data"]]

    def embed_query(self, text: str) -> List[float]:
        payload = json.dumps({"input": text})
        ret = httpx.post(self.url, data=payload, timeout=None)
        ret.raise_for_status()
        return ret.json()["data"][0]["embedding"]


class CustomBedrockEmbeddings(BedrockEmbeddings):
    """
    In order to set temperature, top_p and top_k as settings in the CheshireCat FE we need to re-elaborate those
    parameters and put them into a model_kwargs dict that we will pass to BedrockChat
    """

    def __init__(self, model_id, temperature, top_p, top_k, **kwargs: Any):
        super().__init__(
            model_id=model_id,
            model_kwargs={
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
            },
            **kwargs
        )